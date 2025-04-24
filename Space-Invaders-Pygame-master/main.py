import math
import pygame 
import random
import sys
import json
import time
pygame.init()

pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")

# Ícono
icono = pygame.image.load('ovni.jpg')
pygame.display.set_icon(icono)

# Enemigos por fila
imagen_alien = pygame.transform.scale(pygame.image.load('alien.png'), (40, 30))
imagen_alien1 = pygame.transform.scale(pygame.image.load('alien1.png'), (40, 30))

# Nave Misteriosa
imagen_misterio = pygame.transform.scale(pygame.image.load('misterio.png'), (50, 30))
misterio_x = -80  # Fuera de pantalla
misterio_y = 35
misterio_vel = 0.25
misterio_activo = False
tiempo_ultimo_misterio = pygame.time.get_ticks()
intervalo_misterio = 10000  # 10 segundos

# Fuentes
fuente_menu = pygame.font.Font("arcade.ttf", 40)
# Jugador 
imagen_jugador_original = pygame.image.load('jugador.png')
imagen_jugador = pygame.transform.scale(imagen_jugador_original, (55, 50))
jugador_x = 400
jugador_y = 520
jugador_x_cambio = 0
jugador_velocidad = 0.45
vidas = 3
#Bala
imagen_bala_original = pygame.image.load('bala.png')
imagen_bala = pygame.transform.scale(imagen_bala_original, (40, 40))
bala_x = 0
bala_y = jugador_y
bala_y_cambio = 0.5
bala_estado = "lista"
#Puntaje
puntaje = 0
fuente = pygame.font.Font('arcade.ttf', 22)# Enemigo animado que usabas

def mostrar_puntajes():
    # Esta es la función que muestra los puntajes
    puntajes = obtener_puntajes_json()  # Asumiendo que tienes esta función
    pantalla.fill((0, 0, 0))
    titulo = fuente_menu.render("Puntajes", True, AMARILLO)
    pantalla.blit(titulo, (300, 50))

    for i, entrada in enumerate(sorted(puntajes, key=lambda x: x["puntaje"], reverse=True)):
        texto = fuente.render(f"{entrada['nombre']}: {entrada['puntaje']}", True, BLANCO)
        pantalla.blit(texto, (300, 150 + i * 30))

    pygame.display.update()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                esperando = False  # Regresar al menú de inicio
# Mostrar Puntaje
def mostrar_puntaje():
    texto = fuente.render("Puntaje " + str(puntaje), True, AMARILLO)
    pantalla.blit(texto, (10, 10))
# Vidas
def mostrar_vidas():
    texto = fuente.render("Vidas  " + str(vidas), True, AZUL)
    pantalla.blit(texto, (710, 570))
# Mostrar fin de juego
def mostrar_fin_de_juego():
    pantalla.fill(NEGRO)
    texto_game_over = fuente_menu.render("FIN  DEL JUEGO", True, AMARILLO)
    pantalla.blit(texto_game_over, (250, 250))
    pygame.display.update()
    pygame.mixer.music.stop()
    nombre_jugador = "Jugador1"  # Podrías hacer un input en una pantalla de Game Over
    guardar_puntaje_json(nombre_jugador, puntaje)

    # Guardar el tiempo actual
    tiempo_inicio = pygame.time.get_ticks()

    # Esperar 2 segundos sin congelar el juego
    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Si pasaron 2000 milisegundos (2 segundos)
        if pygame.time.get_ticks() - tiempo_inicio > 1000:
            esperando = False


# Enemigos
imagen_enemigo_1 = pygame.transform.scale(pygame.image.load('enemigos.png'), (45, 35))
imagen_enemigo_2 = pygame.transform.scale(pygame.image.load('enemigos1.png'), (45, 35))
imagenes_enemigo = [imagen_enemigo_1, imagen_enemigo_2]
indice_animacion = 0 
filas = 3
columnas = 10
enemigos = []
inicio_x = 100
inicio_y = 70
espaciado_x = 60
espaciado_y = 50
direccion = 1
vel_x = 0.12
vel_y = 11

for fila in range(filas):
    for columna in range(columnas):
        if fila == 0:
            imagen = imagen_alien
        elif fila == 1:
            imagen = imagen_alien1
        else:
            imagen = imagenes_enemigo[0]  # Primer fotograma de animación

        enemigos.append({
            "x": inicio_x + columna * espaciado_x,
            "y": inicio_y + fila * espaciado_y,
            "fila": fila,
            "vivo": True,
            "imagen": imagen
        })

def guardar_puntaje(nombre, puntaje):
    with open("puntajes.txt", "a") as archivo:
        archivo.write(f"{nombre}:{puntaje}\n")

# Bala
imagen_bala_enemigo = pygame.transform.flip(imagen_bala, False, True)
balas_enemigas = []
tiempo_ultimo_disparo = 0
# Muros
imagenes_muros = {
    1: pygame.transform.scale(pygame.image.load('Murotarribaizquierdaderechaymedio,izquierdayderechamedioymedio.png'), (70, 60)),
    2: pygame.transform.scale(pygame.image.load('Murotarribaizquierdaderechaymedio.png'), (70, 60)),
    3: pygame.transform.scale(pygame.image.load('Murotarribaizquierdayderecha.png'), (70, 60)),
    4: pygame.transform.scale(pygame.image.load('Murotarribaderecha.png'), (70, 60)),
    5: pygame.transform.scale(pygame.image.load('Muro.png'), (70, 60))}
muros = [
    {"x": 193, "y": 450, "salud": 5},
    {"x": 393, "y": 450, "salud": 5},
    {"x": 593, "y": 450, "salud": 5}]

def dibujar_muros():
    for muro in muros:
        if muro["salud"] > 0:
            imagen = imagenes_muros.get(muro["salud"], imagenes_muros[1])
            pantalla.blit(imagen, (muro["x"], muro["y"]))

# Sonidos
sonido_laser = pygame.mixer.Sound('laser.wav')
canal_laser = pygame.mixer.Channel(1) 
sonido_laser.set_volume(0.3)
volumen = 0.05
# Colores
BLANCO = (255, 255, 255)
GRIS = (100, 100, 100)
AZUL = (0, 128, 255)
AMARILLO = (255, 231, 68)
NEGRO = (0, 0, 0)

# Botón
def dibujar_boton(texto, x, y, ancho, alto, activo):
    color = NEGRO
    pygame.draw.rect(pantalla, color, (x, y, ancho, alto))
    etiqueta = fuente_menu.render(texto, True, BLANCO)
    pantalla.blit(etiqueta, (x + 20, y + 10))

# Titulo
imagen_titulo = pygame.image.load('titulo.png') 
imagen_titulo = pygame.transform.scale(imagen_titulo, (600, 150))

def guardar_puntaje_json(nombre, puntaje):
    try:
        with open("puntajes.json", "r") as archivo:
            puntajes = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        puntajes = []

    puntajes.append({"nombre": nombre, "puntaje": puntaje})

    with open("puntajes.json", "w") as archivo:
        json.dump(puntajes, archivo, indent=4)

def obtener_puntajes_json():
    try:
        with open("puntajes.json", "r") as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


# Pantalla de Inicio
def pantalla_inicio():
    en_menu = True
    opciones = ["Jugar", "Como jugar", "Configuracion", "Salir"]
    botones = []   
    ancho_boton = 200
    alto_boton = 70
    centro_x = (800 - ancho_boton) // 2
    inicio_y = 250 

    for i, opcion in enumerate(opciones):
        rect = pygame.Rect(centro_x, inicio_y + i * 50, ancho_boton, alto_boton)
        botones.append((opcion, rect))

    click_procesado = False

    while en_menu:
        pantalla.fill((0, 0, 0)) 
        pantalla.blit(imagen_titulo, (100, 30)) 
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        for opcion, rect in botones:
            activo = rect.collidepoint(mouse_pos)
            color = NEGRO
            pygame.draw.rect(pantalla, color, rect)
            etiqueta = fuente_menu.render(opcion, True, AMARILLO)
            etiqueta_rect = etiqueta.get_rect(center=rect.center)
            pantalla.blit(etiqueta, etiqueta_rect)

            if activo and mouse_click[0] and not click_procesado:
                click_procesado = True
                if opcion == "Jugar":
                    en_menu = False  # Salir del menú de inicio
                elif opcion == "Como jugar":
                    pantalla_como_jugar()
                elif opcion == "Configuracion":
                    pantalla_configuracion()
                elif opcion == "Salir":
                    pygame.quit()
                    exit()

        if not mouse_click[0]:
            click_procesado = False

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    en_menu = False

        pygame.display.update()
    
    
    juego()


def pantalla_como_jugar():
    mostrando = True
    while mostrando:
        pantalla.fill((0, 0, 0))
        instrucciones = [
            "Utiliza las flechas Izquierda y Derecha para moverte",
            "Espacio para disparar",
            "Intenta que las balas no te alcancen",
            "Podes protegerte con los muros",
            "Presiona ESCAPE para volver al menu de inicio"
        ]
        for i, linea in enumerate(instrucciones):
            texto = fuente.render(linea, True, BLANCO)
            pantalla.blit(texto, (200, 150 + i * 40))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                mostrando = False

        pygame.display.update()

def pantalla_configuracion():
    global volumen
    mostrando = True

    barra_x = 250
    barra_y = 300
    barra_ancho = 300
    barra_alto = 20

    while mostrando:
        pantalla.fill((0, 0, 0))

        # Texto del volumen
        texto = fuente.render(f"Volumen {int(volumen * 100)} Porciento", True, AMARILLO)
        pantalla.blit(texto, (300, 200))

        instrucciones = [
                    "Utiliza las flechas Arriba y Abajo para subir o bajar el volumen",
                    "Click para mover o bajar el volumen",
                        ]
        for i, linea in enumerate(instrucciones):
                texto = fuente.render(linea, True, BLANCO)
                pantalla.blit(texto, (100, 300 + i * 40))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    mostrando = False
                elif evento.key == pygame.K_UP:
                    volumen = min(1.0, volumen + 0.05)
                elif evento.key == pygame.K_DOWN:
                    volumen = max(0.0, volumen - 0.05)

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if (barra_x <= mouse_x <= barra_x + barra_ancho and
                    barra_y <= mouse_y <= barra_y + barra_alto):
                    volumen = (mouse_x - barra_x) / barra_ancho
                    volumen = max(0.0, min(1.0, volumen))  # Asegura que esté en rango

        # Actualizar volumen de la música y efectos
        pygame.mixer.music.set_volume(volumen)
        sonido_laser.set_volume(volumen)

        pygame.display.update()
pantalla_inicio()

# Música de fondo y sonidos
pygame.mixer.music.load('fondo.mp3')
pygame.mixer.music.set_volume(volumen)
pygame.mixer.music.play(-1)  # Reproduce en bucle
tiempo_ultima_animacion = pygame.time.get_ticks()
intervalo_animacion = 500  # milisegundos

# Bucle principal del juego
def juego():
    en_pausa = False
    jugando = True
    while jugando:
        pantalla.fill((0, 0, 0))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    jugador_x_cambio = -jugador_velocidad
                elif evento.key == pygame.K_RIGHT:
                    jugador_x_cambio = jugador_velocidad
                elif evento.key == pygame.K_SPACE and bala_estado == "lista":
                    bala_x = jugador_x + 15
                    bala_y = jugador_y
                    bala_estado = "disparando"
                    canal_laser.play(sonido_laser, maxtime=300)
                elif evento.key == pygame.K_p:
                    en_pausa = not en_pausa
            elif evento.type == pygame.KEYUP:
                if evento.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    jugador_x_cambio = 0

        if en_pausa:
            pygame.mixer.music.pause()
            texto_pausa = fuente_menu.render("PAUSA", True, AMARILLO)
            pantalla.blit(texto_pausa, (350, 250))
            pygame.display.update()

            # Esperar a que se presione 'P' de nuevo para salir de pausa
            pausado = True
            while pausado:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_p:
                            pausado = False

            # Contador regresivo antes de volver al juego
            for cuenta_atras in range(3, 0, -1):
                pantalla.fill(NEGRO)
                texto_contador = fuente_menu.render(str(cuenta_atras), True, AMARILLO)
                pantalla.blit(texto_contador, (380, 250))
                pygame.display.update()
                pygame.time.delay(1000)          
            en_pausa = False
            pygame.mixer.music.unpause()
            continue  # Saltar el resto del bucle y volver a iterar

        # Movimiento del jugador
        jugador_x += jugador_x_cambio
        jugador_x = max(0, min(jugador_x, 800 - 50))  # Limitar a los bordes
        pantalla.blit(imagen_jugador, (jugador_x, jugador_y))

        # Tiempo actual (se usa para animaciones y disparos)
        tiempo_actual = pygame.time.get_ticks()

        # Disparo enemigo lento
        if tiempo_actual - tiempo_ultimo_disparo > 800:
            enemigos_primera_fila = [e for e in enemigos if e["vivo"] and e["fila"] == 0]
            if enemigos_primera_fila:
                atacante = random.choice(enemigos_primera_fila)
                balas_enemigas.append({"x": atacante["x"] + 10, "y": atacante["y"] + 20})
                tiempo_ultimo_disparo = tiempo_actual
                canal_laser.play(sonido_laser, maxtime=300)

        # Movimiento en bloque de enemigos
        enemigos_vivos = [e for e in enemigos if e["vivo"]]
        if enemigos_vivos:
            min_x = min(e["x"] for e in enemigos_vivos)
            max_x = max(e["x"] for e in enemigos_vivos)
            if min_x + direccion * vel_x < 0 or max_x + direccion * vel_x > 800 - 35:
                direccion *= -1
                for e in enemigos:
                    if e["vivo"]:
                        e["y"] += vel_y

        # Actualizar animación enemigos
        if tiempo_actual - tiempo_ultima_animacion > intervalo_animacion:
            indice_animacion = (indice_animacion + 1) % len(imagenes_enemigo)
            tiempo_ultima_animacion = tiempo_actual

        # Dibujar enemigos
        for enemigo in enemigos:
            if enemigo["vivo"]:
                enemigo["x"] += direccion * vel_x
                imagen_actual = imagenes_enemigo[indice_animacion] if enemigo["fila"] >= 2 else enemigo["imagen"]
                pantalla.blit(imagen_actual, (enemigo["x"], enemigo["y"]))

                # Fin del juego si bajan
                if vidas <= 0:
                    mostrar_fin_de_juego()
                    pantalla_inicio()
                    pygame.display.update()
                    time.sleep(2)
                    

                # Colisión con bala del jugador
                if bala_estado == "disparando":
                    distancia = math.hypot(enemigo["x"] - bala_x, enemigo["y"] - bala_y)
                    if distancia < 27:
                        enemigo["vivo"] = False
                        bala_y = jugador_y
                        bala_estado = "lista"
                        puntaje += 1
        
        # Movimiento de la bala del jugador
        if bala_estado == "disparando":
            pantalla.blit(imagen_bala, (bala_x, bala_y))
            bala_y -= bala_y_cambio
            if bala_y <= 0:
                bala_y = jugador_y
                bala_estado = "lista"

        # Movimiento de balas enemigas y colisiones
        for bala in balas_enemigas[:]:
            bala["y"] += bala_y_cambio
            pantalla.blit(imagen_bala_enemigo, (bala["x"], bala["y"]))

            # Colisión con jugador
            if jugador_x < bala["x"] < jugador_x + 50 and jugador_y < bala["y"] < jugador_y + 50:
                vidas -= 1
                balas_enemigas.remove(bala)
                if vidas <= 0:
                    mostrar_fin_de_juego()
                    jugando = False
                    pantalla_inicio()


            # Colisión con muros
            for muro in muros:
                if muro["salud"] > 0 and muro["x"] < bala["x"] < muro["x"] + 50 and muro["y"] < bala["y"] < muro["y"] + 40:
                    muro["salud"] -= 1
                    balas_enemigas.remove(bala)
                    break

            # Si sale de pantalla
            if bala["y"] > 600:
                balas_enemigas.remove(bala)
        
            tiempo_actual = pygame.time.get_ticks()

            if not misterio_activo and tiempo_actual - tiempo_ultimo_misterio > intervalo_misterio:
                misterio_x = -80
                misterio_activo = True
                tiempo_ultimo_misterio = tiempo_actual

            # Mover y dibujar nave misteriosa si está activa
            if misterio_activo:
                misterio_x += misterio_vel
                pantalla.blit(imagen_misterio, (misterio_x, misterio_y))

                # Si sale de pantalla, desactivarla
                if misterio_x > 800:
                    misterio_activo = False

                # Colisión con la bala del jugador
                if bala_estado == "disparando":
                    distancia = math.hypot(misterio_x - bala_x, misterio_y - bala_y)
                    if distancia < 30:
                        puntaje += 10
                        misterio_activo = False
                        bala_y = jugador_y
                        bala_estado = "lista"
        # Dibujar muros
        dibujar_muros()

        # Mostrar HUD
        mostrar_puntaje()
        mostrar_vidas()
        pygame.display.update() 
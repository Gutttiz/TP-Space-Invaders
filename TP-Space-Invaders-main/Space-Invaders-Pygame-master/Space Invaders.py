import math
import pygame 
import random
import sys
import json
import os
os.system("cls")
import time
pygame.init()

ARCHIVO_PUNTAJES = "puntajes.json"

# Fuentes
fuente_menu = pygame.font.Font("arcade.ttf", 40)
pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")

# Ícono
icono = pygame.image.load('ovni.jpg')
pygame.display.set_icon(icono)

# Titulo
imagen_titulo = pygame.image.load('titulo.png') 
imagen_titulo = pygame.transform.scale(imagen_titulo, (600, 150))

# Jugador 
imagen_jugador_original = pygame.image.load('jugador.png')
imagen_jugador = pygame.transform.scale(imagen_jugador_original, (55, 30))
jugador_x = 385
jugador_y = 520
jugador_x_cambio = 0
jugador_velocidad = 0.4
vidas = 3

# Enemigos
imagen_enemigo_1 = pygame.transform.scale(pygame.image.load('enemigos.png'), (45, 35))
imagen_enemigo_2 = pygame.transform.scale(pygame.image.load('enemigos1.png'), (45, 35))
imagen_alien = pygame.transform.scale(pygame.image.load('alien.png'), (40, 30))
imagen_alien2 = pygame.transform.scale(pygame.image.load('alien2.png'), (40, 30))
imagen_alien1 = pygame.transform.scale(pygame.image.load('alien1.png'), (40, 30))
imagen_alien12 = pygame.transform.scale(pygame.image.load('alien12.png'), (40, 30))
imagenes_enemigo = [imagen_enemigo_1, imagen_enemigo_2]
imagenes_alien1 = [imagen_alien, imagen_alien2]
imagenes_alien2 = [imagen_alien1, imagen_alien12]
indice_animacion = 0 
filas = 3
columnas = 10
enemigos = []
inicio_x = 100
inicio_y = 70
espaciado_x = 60
espaciado_y = 50
direccion = 1
vel_x = 0.1
vel_y = 8

# Nave Misteriosa
imagen_misterio = pygame.transform.scale(pygame.image.load('misterio.png'), (50, 30))
misterio_x = -80  # Fuera de pantalla
misterio_y = 35
misterio_vel = 0.145
misterio_activo = False
tiempo_ultimo_misterio = pygame.time.get_ticks()
intervalo_misterio = 10000  # 10 segundos

#Bala
imagen_bala_original = pygame.image.load('bala.png')
imagen_bala = pygame.transform.scale(imagen_bala_original, (10, 30))
bala_x = 0
bala_y = jugador_y
bala_y_cambio = 0.4
bala_estado = "lista"

# Bala invertida
imagen_bala_enemigo = pygame.transform.flip(imagen_bala, False, True)
balas_enemigas = []
tiempo_ultimo_disparo = 0

# Muros
imagenes_muros = {
    1: pygame.transform.scale(pygame.image.load('Muro5.png'), (60, 40)),
    2: pygame.transform.scale(pygame.image.load('Muro4.png'), (60, 40)),
    3: pygame.transform.scale(pygame.image.load('Muro3.png'), (60, 40)),
    4: pygame.transform.scale(pygame.image.load('Muro2.png'), (60, 40)),
    5: pygame.transform.scale(pygame.image.load('Muro1.png'), (60, 40))}
muros = [
    {"x": 185, "y": 450, "salud": 5},
    {"x": 385, "y": 450, "salud": 5},
    {"x": 585, "y": 450, "salud": 5}]

# Sonidos
sonido_laser = pygame.mixer.Sound('laser.wav')
canal_laser = pygame.mixer.Channel(1) 
sonido_laser.set_volume(0.3)
volumen = 0.05

# Música de fondo y sonidos
pygame.mixer.music.load('fondo.mp3')
pygame.mixer.music.set_volume(volumen)
pygame.mixer.music.play(-1)  # Reproduce en bucle
tiempo_ultima_animacion = pygame.time.get_ticks()
intervalo_animacion = 500  # milisegundos

# Colores
BLANCO = (255, 255, 255)
GRIS = (100, 100, 100)
AZUL = (0, 128, 255)
AMARILLO = (255, 231, 68)
NEGRO = (0, 0, 0)

#Puntaje
puntaje = 0
fuente = pygame.font.Font('arcade.ttf', 22)

#Definiciones
def mostrar_puntaje():
    texto = fuente.render("Puntaje   " + str(puntaje), True, AMARILLO)
    pantalla.blit(texto, (10, 10))

def cargar_puntajes():
    try:
        with open(ARCHIVO_PUNTAJES, "r") as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Si no existe el archivo o está vacío, devuelve una lista vacía

# Pantalla para mostrar los puntajes
def guardar_puntaje(nombre, puntaje):
    """
    Guarda el puntaje del jugador en un archivo JSON.
    Si el archivo no existe, lo crea.
    """
    try:
        # Cargar puntajes existentes
        with open(ARCHIVO_PUNTAJES, "r") as archivo:
            puntajes = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        # Si el archivo no existe o está vacío, inicializar una lista vacía
        puntajes = []

    # Agregar el nuevo puntaje
    puntajes.append({"nombre": nombre, "puntaje": puntaje})

    # Guardar los puntajes actualizados en el archivo
    with open(ARCHIVO_PUNTAJES, "w") as archivo:
        json.dump(puntajes, archivo, indent=4)
        
def pantalla_puntajes():
    mostrando = True
    puntajes = cargar_puntajes()
    puntajes_ordenados = sorted(puntajes, key=lambda x: x["puntaje"], reverse=True)  # Ordenar por puntaje descendente

    while mostrando:
        pantalla.fill(NEGRO)
        texto_titulo = fuente_menu.render("PUNTAJES", True, AMARILLO)
        pantalla.blit(texto_titulo, (300, 50))

        # Mostrar los puntajes
        for i, entrada in enumerate(puntajes_ordenados[:10]):  # Mostrar los 10 mejores puntajes
            texto = fuente.render(f"{i + 1}. {entrada['nombre']}: {entrada['puntaje']}", True, BLANCO)
            pantalla.blit(texto, (200, 150 + i * 30))

        texto_volver = fuente.render("Presiona ESC para volver", True, GRIS)
        pantalla.blit(texto_volver, (250, 500))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                mostrando = False

        pygame.display.update()

def reiniciar():
    global jugador_x, jugador_y, jugador_x_cambio, vidas, bala_x, bala_y, bala_estado, enemigos, balas_enemigas, direccion, misterio_x, misterio_y, misterio_activo
    jugador_x_cambio = 0
    jugador_x = 385
    jugador_y = 520
    vidas = 3
    bala_x = 0
    bala_y = jugador_y  # Mantener la misma posición de y para la bala
    bala_estado = "lista"
    balas_enemigas.clear()
    direccion = 1
    misterio_x = -80
    misterio_y = 35
    misterio_activo = False

    enemigos.clear()
    for fila in range(filas):
        for columna in range(columnas):
            if fila == 0:
                imagen = imagen_alien
            elif fila == 1:
                imagen = imagen_alien1
            else:
                imagen = imagenes_enemigo[0]
            enemigos.append({
                "x": inicio_x + columna * espaciado_x,
                "y": inicio_y + fila * espaciado_y,
                "fila": fila,
                "vivo": True,
                "imagen": imagen
            })
    for muro in muros:
        muro["salud"] = 5
def reiniciar_juego():
    global jugador_x, jugador_y, jugador_x_cambio, vidas, bala_x, bala_y, bala_estado, enemigos, balas_enemigas, direccion, misterio_x, misterio_y, misterio_activo
    jugador_x_cambio = 0
    jugador_y = 520
    vidas = 3
    bala_x = 0
    bala_y = jugador_y  # Mantener la misma posición de y para la bala
    bala_estado = "lista"
    balas_enemigas.clear()
    direccion = 1
    misterio_x = -80
    misterio_y = 35
    misterio_activo = False

    enemigos.clear()
    for fila in range(filas):
        for columna in range(columnas):
            if fila == 0:
                imagen = imagen_alien
            elif fila == 1:
                imagen = imagen_alien1
            else:
                imagen = imagenes_enemigo[0]
            enemigos.append({
                "x": inicio_x + columna * espaciado_x,
                "y": inicio_y + fila * espaciado_y,
                "fila": fila,
                "vivo": True,
                "imagen": imagen
            })
    #for muro in muros:
    #    muro["salud"] = 5



def mostrar_vidas():
    texto = fuente.render("Vidas  " + str(vidas), True, AZUL)
    pantalla.blit(texto, (710, 570))

def mostrar_fin_de_juego():
    global puntaje
    pantalla.fill(NEGRO)
    pygame.mixer.music.pause()
    texto_game_over = fuente_menu.render("FIN DEL JUEGO", True, AMARILLO)
    pantalla.blit(texto_game_over, (275, 275))
    pygame.display.update()
    tiempo_inicio = pygame.time.get_ticks()

    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if pygame.time.get_ticks() - tiempo_inicio > 1000:
            esperando = False

    # Pedir el nombre del jugador
    nombre = pedir_nombre()
    guardar_puntaje(nombre, puntaje)


def pedir_nombre():
    nombre = ""
    ingresando = True
    while ingresando:
        pantalla.fill(NEGRO)
        texto = fuente_menu.render("Ingresa tu nombre:", True, AMARILLO)
        pantalla.blit(texto, (200, 200))
        texto_nombre = fuente_menu.render(nombre, True, BLANCO)
        pantalla.blit(texto_nombre, (200, 300))
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:  # Enter para confirmar
                    ingresando = False
                elif evento.key == pygame.K_BACKSPACE:  # Borrar último carácter
                    nombre = nombre[:-1]
                else:
                    nombre += evento.unicode  # Agregar carácter

    return nombre
#Colocacion de aliens en las filas y columnas
for fila in range(filas):
    for columna in range(columnas):
        if fila == 0:
            imagen = imagen_alien
        elif fila == 1:
            imagen = imagen_alien1
        else:
            imagen = imagenes_enemigo[0] 

        enemigos.append({
            "x": inicio_x + columna * espaciado_x,
            "y": inicio_y + fila * espaciado_y,
            "fila": fila,
            "vivo": True,
            "imagen": imagen
        })

def dibujar_muros():
    for muro in muros:
        if muro["salud"] > 0:
            imagen = imagenes_muros.get(muro["salud"], imagenes_muros[1])
            pantalla.blit(imagen, (muro["x"], muro["y"]))

def pantalla_inicio():
    global en_menu, puntaje
    puntaje = 0
    en_menu = True
    opciones = ["Jugar", "Puntajes", "Como jugar", "Configuracion", "Salir"]
    botones = []   
    ancho_boton = 200
    alto_boton = 70
    centro_x = (800 - ancho_boton) // 2
    inicio_y = 250 
    pygame.mixer.music.pause()
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
                    en_menu = False
                    pygame.mixer.music.unpause()
                elif opcion == "Puntajes":
                    pantalla_puntajes()
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

def pantalla_como_jugar():
    mostrando = True
    while mostrando:
        pantalla.fill((0, 0, 0))
        instrucciones = [
            "Utiliza  las  flechas  Izquierda  y  Derecha  para  moverte",
            "Espacio  para disparar",
            "Intenta  que  las  balas  no  te  alcancen",
            "Podes  protegerte  con  los  muros",
            "Presiona  ESCAPE  para  volver  al  menu  de  inicio"
        ]
        for i, linea in enumerate(instrucciones):
            texto = fuente.render(linea, True, AMARILLO)
            pantalla.blit(texto, (120, 200 + i * 40))

        # Agregar un título a la pantalla de instrucciones
        titulo = fuente_menu.render("COMO JUGAR", True, AMARILLO)
        pantalla.blit(titulo, (300, 50))

        # Agregar un botón visual para volver al menú
        texto_volver = fuente.render("Presiona ESC para volver", True, GRIS)
        pantalla.blit(texto_volver, (250, 500))

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

        texto = fuente.render(f"Volumen   {int(volumen * 100)}   Porciento", True, AMARILLO)
        pantalla.blit(texto, (300, 200))

        instrucciones = [
            "Utiliza las flechas Arriba y Abajo para subir o bajar el volumen",
            "Click para subir o bajar el volumen",
            "Presiona R para restablecer el volumen predeterminado",
            "Presiona ESC para volver al menú principal"
        ]
        for i, linea in enumerate(instrucciones):
            texto = fuente.render(linea, True, AMARILLO)
            pantalla.blit(texto, (69, 350 + i * 30))

        # Dibujar barra de volumen
        pygame.draw.rect(pantalla, GRIS, (barra_x, barra_y, barra_ancho, barra_alto))
        pygame.draw.rect(pantalla, AZUL, (barra_x, barra_y, int(volumen * barra_ancho), barra_alto))

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
                elif evento.key == pygame.K_r:  # Restablecer volumen predeterminado
                    volumen = 0.05

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

#Main
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
                bala_x = jugador_x + 25
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
        # Definir botones
        boton_reanudar = pygame.Rect(300, 300, 200, 60)
        boton_volver_menu = pygame.Rect(300, 400, 200, 60)
        boton_salir = pygame.Rect(300, 500, 200, 60)  # Nuevo botón

        pausado = True
        reanudar_juego = False  # Variable para controlar si se debe reanudar el juego

        while pausado:
            pantalla.fill(NEGRO)

            # Título de pausa
            texto_pausa = fuente_menu.render("PAUSA", True, AMARILLO)
            rect_pausa = texto_pausa.get_rect(center=(800 // 2, 100))
            pantalla.blit(texto_pausa, rect_pausa)

            # Botones
            pygame.draw.rect(pantalla, NEGRO, boton_reanudar)
            pygame.draw.rect(pantalla, NEGRO, boton_volver_menu)
            pygame.draw.rect(pantalla, NEGRO, boton_salir)
              # Dibujar el nuevo botón

            texto_reanudar = fuente_menu.render("Reanudar", True, AMARILLO)
            texto_salir = fuente_menu.render("Salir", True, AMARILLO)
            texto_volver_menu = fuente_menu.render("Menu", True, AMARILLO)  # Texto del nuevo botón

            pantalla.blit(texto_reanudar, texto_reanudar.get_rect(center=boton_reanudar.center))
            pantalla.blit(texto_salir, texto_salir.get_rect(center=boton_salir.center))
            pantalla.blit(texto_volver_menu, texto_volver_menu.get_rect(center=boton_volver_menu.center))  # Mostrar texto

            pygame.display.update()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if boton_reanudar.collidepoint(evento.pos):
                        reanudar_juego = True  # Indicar que se debe reanudar el juego
                        pausado = False
                    elif boton_salir.collidepoint(evento.pos):
                        pygame.quit()
                        sys.exit()
                    elif boton_volver_menu.collidepoint(evento.pos):  # Manejar clic en el nuevo botón
                        reiniciar_juego()  # Llamar a la función para reiniciar enemigos
                        pausado = False
                        en_pausa = False
                        pantalla_inicio()  # Llamar a la función para regresar al menú principal

                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_p:
                        reanudar_juego = True  # Indicar que se debe reanudar el juego
                        pausado = False

        # Contador regresivo antes de volver al juego (solo si se seleccionó "Reanudar")
        if reanudar_juego:
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
            if enemigo["fila"] >= 2:
                imagen_actual = imagenes_enemigo[indice_animacion]
            elif enemigo["fila"] == 1:
                imagen_actual = imagenes_alien2[indice_animacion]
            elif enemigo["fila"] == 0:
                imagen_actual = imagenes_alien1[indice_animacion]

            pantalla.blit(imagen_actual, (enemigo["x"], enemigo["y"]))

            # Fin del juego si bajan
            if enemigo["y"] > 420:
                mostrar_fin_de_juego()
                pantalla_inicio()
                reiniciar()
            if vidas <= 0 and en_menu == True:
                mostrar_fin_de_juego()
                pygame.display.update()        
                pantalla_inicio() 
    
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

        # Colisión de bala del jugador con muros
        for muro in muros:
            if muro["salud"] > 0 and muro["x"] < bala_x < muro["x"] + 64 and muro["y"] < bala_y < muro["y"] + 54:
                muro["salud"] -= 1
                bala_y = jugador_y
                bala_estado = "lista"
                break

        # Si sale de pantalla
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
                reiniciar()
                pantalla_inicio()
                
        
        # Colisión con muros
        for muro in muros:
            if muro["salud"] > 0 and muro["x"] < bala["x"] < muro["x"] + 64 and muro["y"] < bala["y"] < muro["y"] + 40:
                muro["salud"] -= 1
                balas_enemigas.remove(bala)
                break
    
        # Si sale de pantalla
        if bala["y"] > 620:
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

    if bala_estado == "disparando":
            distancia = math.hypot(misterio_x - bala_x, misterio_y - bala_y)
            if distancia < 30:
                    puntaje += 10
                    misterio_activo = False
                    bala_y = jugador_y
                    bala_estado = "lista"
    # Comprobar si todos los enemigos han sido derrotados
    if all(not e["vivo"] for e in enemigos):
        reiniciar_juego()  # Reinicia el juego, incluyendo los enemigos

    # Dibujar muros
    dibujar_muros()

    # Mostrar HUD
    mostrar_puntaje()
    mostrar_vidas()
    pygame.display.update() 
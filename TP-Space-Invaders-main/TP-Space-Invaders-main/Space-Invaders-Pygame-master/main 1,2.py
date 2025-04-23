import math
import pygame 
import random
pygame.init()

pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")

# Ícono
icono = pygame.image.load('ovni.jpg')
pygame.display.set_icon(icono)

# Fuentes
fuente_menu = pygame.font.Font("arcade.ttf", 40)
# Jugador 
imagen_jugador_original = pygame.image.load('jugador.png')
imagen_jugador = pygame.transform.scale(imagen_jugador_original, (55, 55))
jugador_x = 400
jugador_y = 540
jugador_x_cambio = 0
jugador_velocidad = 0.45
vidas = 3
#Bala
imagen_bala_original = pygame.image.load('bala.png')
imagen_bala = pygame.transform.scale(imagen_bala_original, (30, 30))
bala_x = 0
bala_y = jugador_y
bala_y_cambio = 0.5
bala_estado = "lista"
#Puntaje
puntaje =  0
fuente = pygame.font.Font('arcade.ttf', 22)
# Mostrar Puntaje
def mostrar_puntaje():
    texto = fuente.render("Puntaje " + str(puntaje), True, AMARILLO)
    pantalla.blit(texto, (10, 10))
# Vidas
def mostrar_vidas():
    texto = fuente.render("Vidas  " + str(vidas), True, AZUL)
    pantalla.blit(texto, (680, 560))
# Mostrar fin de juego
def mostrar_fin_de_juego():
    fuente_final = pygame.font.Font('arcade.ttf', 50)
    texto = fuente_final.render("FIN DEL JUEGO", True, AMARILLO)
    pantalla.blit(texto, (200, 250))
# Pantalla de Pausa
def pantalla_pausa():
    global en_pausa
    en_pausa = True
    while en_pausa:
        pantalla.fill((0, 0, 0))  # Fondo negro

        # Título de Pausa
        texto_pausa = fuente_menu.render("PAUSA", True, AMARILLO)
        pantalla.blit(texto_pausa, (350, 250))  # Mostrar título "PAUSA"

        # Botones "Reanudar" y "Volver al menú"
        dibujar_boton("Reanudar", 300, 350, 200, 60, True)
        dibujar_boton("Volver al menu", 300, 450, 200, 60, True)

        # Manejo de eventos (clics del ratón y teclas)
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if 300 <= mouse_pos[0] <= 500 and 350 <= mouse_pos[1] <= 410:  # Reanudar
                    en_pausa = False  # Volver al juego
                    pygame.mixer.music.unpause()  # Reanudar música
                elif 300 <= mouse_pos[0] <= 500 and 450 <= mouse_pos[1] <= 510:  # Volver al menú
                    pygame.mixer.music.stop()  # Detener música
                    pantalla_inicio()  # Regresar al menú
                    en_pausa = False

            # Opción de salir con ESCAPE
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                en_pausa = False  # Volver al juego
                pygame.mixer.music.unpause()  # Reanudar música

        pygame.display.update()  # Actualizar la pantalla

# Enemigos
imagen_enemigo_1 = pygame.transform.scale(pygame.image.load('enemigos.png'), (45, 36))
imagen_enemigo_2 = pygame.transform.scale(pygame.image.load('enemigos1.png'), (45, 36))
imagenes_enemigo = [imagen_enemigo_1, imagen_enemigo_2]
indice_animacion = 0 
filas = 3
columnas = 10
enemigos = []
inicio_x = 100
inicio_y = 50
espaciado_x = 50
espaciado_y = 40
direccion = 1
vel_x = 0.12
vel_y = 11

for fila in range(filas):
    for columna in range(columnas):
        enemigos.append({
            "x": inicio_x + columna * espaciado_x,
            "y": inicio_y + fila * espaciado_y,
            "fila": fila,
            "vivo": True
        })
# Bala
imagen_bala_enemigo = pygame.transform.flip(imagen_bala, False, True)
balas_enemigas = []
tiempo_ultimo_disparo = 0
# Muros
imagenes_muros = {
    1: pygame.transform.scale(pygame.image.load('Murotarribaizquierdaderechaymedio,izquierdayderechamedioymedio.png'), (50, 40)),
    2: pygame.transform.scale(pygame.image.load('Murotarribaizquierdaderechaymedio.png'), (50, 40)),
    3: pygame.transform.scale(pygame.image.load('Murotarribaizquierdayderecha.png'), (50, 40)),
    4: pygame.transform.scale(pygame.image.load('Murotarribaderecha.png'), (50, 40)),
    5: pygame.transform.scale(pygame.image.load('Muro.png'), (50, 40))}
muros = [
    {"x": 200, "y": 400, "salud": 5},
    {"x": 400, "y": 400, "salud": 5},
    {"x": 600, "y": 400, "salud": 5}]

def dibujar_muros():
    for muro in muros:
        if muro["salud"] > 0:
            imagen = imagenes_muros.get(muro["salud"], imagenes_muros[1])
            pantalla.blit(imagen, (muro["x"], muro["y"]))

# Sonidos
sonido_laser = pygame.mixer.Sound('laser.wav')
canal_laser = pygame.mixer.Channel(1) 
sonido_laser.set_volume(0.3)
volumen = 0.1

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
    etiqueta = fuente_menu.render(texto, True, AMARILLO)
    pantalla.blit(etiqueta, (x + 20, y + 10))

# Titulo
imagen_titulo = pygame.image.load('titulo.png') 
imagen_titulo = pygame.transform.scale(imagen_titulo, (600, 150))

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
                    en_menu = False
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
        texto = fuente.render(f"Volumen: {int(volumen * 100)}%", True, AMARILLO)
        pantalla.blit(texto, (310, 200))

        # Instrucciones
        instrucciones = [
            "Flechas ↑ ↓ para subir o bajar el volumen",
            "Click en la barra para ajustar",
            "ESC para volver al menú"
        ]
        for i, linea in enumerate(instrucciones):
            texto = fuente.render(linea, True, BLANCO)
            pantalla.blit(texto, (100, 400 + i * 30))

        # Barra de volumen (fondo)
        pygame.draw.rect(pantalla, GRIS, (barra_x, barra_y, barra_ancho, barra_alto))

        # Parte llena (nivel de volumen)
        ancho_lleno = int(barra_ancho * volumen)
        pygame.draw.rect(pantalla, AMARILLO, (barra_x, barra_y, ancho_lleno, barra_alto))

        # Marco de la barra
        pygame.draw.rect(pantalla, BLANCO, (barra_x, barra_y, barra_ancho, barra_alto), 2)

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
                    volumen = max(0.0, min(1.0, volumen))  # asegurar que esté en rango

        # Aplicar el nuevo volumen a la música y sonidos
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
            elif evento.key == pygame.K_ESCAPE:
                pantalla_pausa()  # Pausar el juego

        elif evento.type == pygame.KEYUP:
            if evento.key in (pygame.K_LEFT, pygame.K_RIGHT):
                jugador_x_cambio = 0

    if en_pausa:
        # La pantalla de pausa ya se maneja en la función pantalla_pausa()
        continue  # No ejecutar más código si el juego está en pausa

    # Continuar con el juego (mismo flujo que ya tienes)
    jugador_x += jugador_x_cambio
    jugador_x = max(0, min(jugador_x, 800 - 50))  # Limitar a los bordes
    pantalla.blit(imagen_jugador, (jugador_x, jugador_y))

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
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - tiempo_ultima_animacion > intervalo_animacion:
            indice_animacion = (indice_animacion + 1) % len(imagenes_enemigo)
            tiempo_ultima_animacion = tiempo_actual

    # Dibujar enemigos
    for enemigo in enemigos:
        if enemigo["vivo"]:
            enemigo["x"] += direccion * vel_x
            pantalla.blit(imagenes_enemigo[indice_animacion], (enemigo["x"], enemigo["y"]))

            # Game Over si bajan demasiado
            if enemigo["y"] > 480:
                mostrar_fin_de_juego()
                jugando = False

            # Colisión con bala del jugador
            if bala_estado == "disparando":
                distancia = math.hypot(enemigo["x"] - bala_x, enemigo["y"] - bala_y)
                if distancia < 27:
                    enemigo["vivo"] = False
                    bala_y = jugador_y
                    bala_estado = "lista"
                    puntaje += 1
                    if not canal_laser.get_busy():
                        canal_laser.play(sonido_laser, maxtime=300)
    # Movimiento de bala del jugador
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

        # Colisión con muros
        for muro in muros:
            if muro["salud"] > 0 and muro["x"] < bala["x"] < muro["x"] + 50 and muro["y"] < bala["y"] < muro["y"] + 40:
                muro["salud"] -= 1
                balas_enemigas.remove(bala)
                break

        # Si la bala sale de la pantalla
        if bala["y"] > 600:
            balas_enemigas.remove(bala)

    # Colisión de bala del jugador con muros
    for muro in muros:
        if muro["salud"] > 0 and muro["x"] < bala_x < muro["x"] + 50 and muro["y"] < bala_y < muro["y"] + 40:
            muro["salud"] -= 1
            bala_y = jugador_y
            bala_estado = "lista"
    

    # Dibujar muros
    dibujar_muros()

    # Mostrar HUD
    mostrar_puntaje()
    mostrar_vidas()
    pygame.display.update()
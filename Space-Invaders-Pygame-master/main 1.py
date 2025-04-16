import math
import pygame
import random

# Inicializar Pygame
pygame.init()

# Crear pantalla
pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")

# Ícono
icono = pygame.image.load('ovni.png')
pygame.display.set_icon(icono)

# Jugador
imagen_jugador_original = pygame.image.load('jugador.png')
imagen_jugador = pygame.transform.scale(imagen_jugador_original, (50, 50))
jugador_x = 370
jugador_y = 520
jugador_x_cambio = 0
jugador_velocidad = 0.7

# Enemigos
imagen_enemigo_original = pygame.image.load('enemigo.png')
imagen_enemigo = pygame.transform.scale(imagen_enemigo_original, (35, 35))
filas = 5
columnas = 11
enemigos = []
inicio_x = 100
inicio_y = 50
espaciado_x = 60
espaciado_y = 50
direccion = 1
vel_x = 0.2
vel_y = 1.1

for fila in range(filas):
    for columna in range(columnas):
        enemigos.append({
            "x": inicio_x + columna * espaciado_x,
            "y": inicio_y + fila * espaciado_y,
            "vivo": True
        })

# Bala del jugador
imagen_bala_original = pygame.image.load('bala.png')
imagen_bala = pygame.transform.scale(imagen_bala_original, (20, 20))
bala_x = 0
bala_y = jugador_y
bala_y_cambio = 0.5
bala_estado = "lista"

# Bala del enemigo (invertida)
imagen_bala_enemigo = pygame.transform.flip(imagen_bala, False, True)
balas_enemigas = []

# Imágenes del muro según salud
imagenes_muros = {
    1: pygame.transform.scale(pygame.image.load('Murotarribaizquierdaderechaymedio,izquierdayderechamedioymedio.png'), (50, 40)),
    2: pygame.transform.scale(pygame.image.load('Murotarribaizquierdaderechaymedio.png'), (50, 40)),
    3: pygame.transform.scale(pygame.image.load('Murotarribaizquierdayderecha.png'), (50, 40)),
    4: pygame.transform.scale(pygame.image.load('Murotarribaderecha.png'), (50, 40)),
    5 : pygame.transform.scale(pygame.image.load('Muro.png'), (50, 40))
}

# Muros
muros = [
    {"x": 200, "y": 400, "salud": 5},
    {"x": 400, "y": 400, "salud": 5},
    {"x": 600, "y": 400, "salud": 5}
]

vidas = 3

# Puntaje
puntaje = 0
fuente = pygame.font.Font('freesansbold.ttf', 24)
def mostrar_vidas():
    texto = fuente.render("Vidas: " + str(vidas), True, (255, 255, 255))
    pantalla.blit(texto, (680, 560))  # Abajo a la derecha

def mostrar_puntaje():
    texto = fuente.render("Puntaje: " + str(puntaje), True, (255, 255, 255))
    pantalla.blit(texto, (10, 10))

def mostrar_game_over():
    fuente_final = pygame.font.Font('freesansbold.ttf', 50)
    texto = fuente_final.render("FIN DEL JUEGO", True, (255, 255, 255))
    pantalla.blit(texto, (200, 250))

def dibujar_muros():
    for muro in muros:
        if muro["salud"] > 0:
            imagen = imagenes_muros.get(muro["salud"], imagenes_muros[1])
            pantalla.blit(imagen, (muro["x"], muro["y"]))

# Bucle principal
jugando = True
while jugando:
    pantalla.fill((0, 0, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -jugador_velocidad
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = jugador_velocidad
            if evento.key == pygame.K_SPACE and bala_estado == "lista":
                bala_x = jugador_x + 15
                bala_estado = "disparando"

        if evento.type == pygame.KEYUP:
            if evento.key in (pygame.K_LEFT, pygame.K_RIGHT):
                jugador_x_cambio = 0
    for bala in balas_enemigas[:]:
        bala["y"] += bala_y_cambio
        pantalla.blit(imagen_bala_enemigo, (bala["x"], bala["y"]))
                # Si te pega una bala enemiga
        if jugador_x < bala["x"] < jugador_x + 50 and jugador_y < bala["y"] < jugador_y + 50:
            vidas -= 1
            balas_enemigas.remove(bala)
            if vidas <= 0:
                mostrar_game_over()
                for e in enemigos:
                    e["vivo"] = False
                jugando = False  # Termina el juego

    # Mover jugador
    jugador_x += jugador_x_cambio
    jugador_x = max(0, min(jugador_x, 800 - 50))
    pantalla.blit(imagen_jugador, (jugador_x, jugador_y))

    # Movimiento de enemigos en bloque
    enemigos_vivos = [e for e in enemigos if e["vivo"]]
    if enemigos_vivos:
        min_x = min(e["x"] for e in enemigos_vivos)
        max_x = max(e["x"] for e in enemigos_vivos)
        if min_x + direccion * vel_x < 0 or max_x + direccion * vel_x > 800 - 35:
            direccion *= -1
            for e in enemigos:
                if e["vivo"]:
                    e["y"] += vel_y

    # Dibujar enemigos
    for enemigo in enemigos:
        if enemigo["vivo"]:
            enemigo["x"] += direccion * vel_x
            pantalla.blit(imagen_enemigo, (enemigo["x"], enemigo["y"]))

            # Fin del juego si bajan demasiado
            if enemigo["y"] > 480:
                for e in enemigos:
                    e["vivo"] = False
                mostrar_game_over()

            # Colisión con bala del jugador
            if bala_estado == "disparando":
                distancia = math.hypot(enemigo["x"] - bala_x, enemigo["y"] - bala_y)
                if distancia < 27:
                    enemigo["vivo"] = False
                    bala_y = jugador_y
                    bala_estado = "lista"
                    puntaje += 1

    # Disparo enemigo aleatorio
    if len(balas_enemigas) < 5 and random.randint(0, 100) < 2:
        enemigos_vivos = [e for e in enemigos if e["vivo"]]
        if enemigos_vivos:
            atacante = random.choice(enemigos_vivos)
            balas_enemigas.append({
                "x": atacante["x"] + 15,
                "y": atacante["y"] + 35
            })

    # Movimiento y dibujo de la bala del jugador
    if bala_estado == "disparando":
        pantalla.blit(imagen_bala, (bala_x, bala_y))
        bala_y -= bala_y_cambio
        if bala_y <= 0:
            bala_y = jugador_y
            bala_estado = "lista"

    # Movimiento y dibujo de balas enemigas
    for bala in balas_enemigas[:]:
        bala["y"] += bala_y_cambio
        pantalla.blit(imagen_bala_enemigo, (bala["x"], bala["y"]))

        if bala["y"] > 600:
            balas_enemigas.remove(bala)

        for muro in muros:
            if muro["salud"] > 0 and muro["x"] < bala["x"] < muro["x"] + 50 and muro["y"] < bala["y"] < muro["y"] + 40:
                muro["salud"] -= 1
                balas_enemigas.remove(bala)
                break

    # Colisión de la bala del jugador con muros
    for muro in muros:
        if muro["salud"] > 0 and muro["x"] < bala_x < muro["x"] + 50 and muro["y"] < bala_y < muro["y"] + 40:
            muro["salud"] -= 1
            bala_y = jugador_y
            bala_estado = "lista"

    # Dibujar muros
    dibujar_muros()

    # Puntaje
    mostrar_puntaje()
    mostrar_vidas()
    pygame.display.update()

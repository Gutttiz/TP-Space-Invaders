import pygame
import random

# Inicializamos pygame
pygame.init()

# Definir colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)

# Dimensiones de la pantalla
ANCHO = 800
ALTO = 600

# Crear la pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Space Invaders")

# Reloj para controlar la velocidad de actualización
reloj = pygame.time.Clock()

# Cargar imágenes
nave_img = pygame.image.load('nave.png')
nave_img = pygame.transform.scale(nave_img, (40, 40))  # Ajustar tamaño de la nave
alien_img = pygame.image.load('Enemigo1.png')
alien_img = pygame.transform.scale(alien_img, (30, 30))  # Ajustar tamaño de los aliens

# Clases del juego

class Nave:
    def __init__(self):
        self.ancho = 40  # Nave más pequeña
        self.alto = 40   # Nave más pequeña
        self.x = ANCHO // 2 - self.ancho // 2
        self.y = ALTO - self.alto - 10
        self.velocidad = 5
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)

    def mover(self, teclas):
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += self.velocidad

    def dibujar(self):
        pantalla.blit(nave_img, (self.rect.x, self.rect.y))  # Dibujar la nave usando la imagen

class Alien:
    def __init__(self, x, y):
        self.ancho = 30  # Enemigos más pequeños
        self.alto = 30   # Enemigos más pequeños
        self.x = x
        self.y = y
        self.velocidad = 2
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        self.direccion = 1  # 1 para mover derecha, -1 para mover izquierda

    def mover(self):
        self.rect.x += self.velocidad * self.direccion

        # Si llega al borde de la pantalla, cambia la dirección y baja
        if self.rect.left <= 0 or self.rect.right >= ANCHO:
            self.direccion *= -1
            self.rect.y += 10  # Baja un poco cuando cambia de dirección

    def dibujar(self):
        pantalla.blit(alien_img, (self.rect.x, self.rect.y))  # Dibujar el alien usando la imagen

    def disparar(self):
        return Proyectil(self.rect.centerx, self.rect.bottom)

class Proyectil:
    def __init__(self, x, y, direccion=-1):
        self.ancho = 5
        self.alto = 10
        self.x = x
        self.y = y
        self.velocidad = 7
        self.direccion = direccion  # -1 para arriba, 1 para abajo
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)

    def mover(self):
        self.rect.y += self.velocidad * self.direccion

    def dibujar(self):
        pygame.draw.rect(pantalla, BLANCO, self.rect)

# Función para la pantalla de inicio
def pantalla_inicio():
    fuente = pygame.font.Font(None, 74)
    fuente_boton = pygame.font.Font(None, 48)
    
    titulo = fuente.render("Space Invaders", True, BLANCO)
    boton_play = fuente_boton.render("Play", True, VERDE)
    boton_score = fuente_boton.render("Score Table", True, VERDE)
    
    # Coordenadas de los elementos
    titulo_rect = titulo.get_rect(center=(ANCHO // 2, ALTO // 4))
    play_rect = boton_play.get_rect(center=(ANCHO // 2, ALTO // 2))
    score_rect = boton_score.get_rect(center=(ANCHO // 2, ALTO // 1.5))
    
    ejecutando = True
    while ejecutando:
        pantalla.fill(NEGRO)

        # Mostrar el título y los botones
        pantalla.blit(titulo, titulo_rect)
        pantalla.blit(boton_play, play_rect)
        pantalla.blit(boton_score, score_rect)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if play_rect.collidepoint(x, y):
                    return 'play'
                if score_rect.collidepoint(x, y):
                    return 'score'

        pygame.display.update()
        reloj.tick(60)

# Función para la pantalla de juego
def juego():
    nave = Nave()
    aliens = [Alien(x * 60 + 50, y * 60 + 50) for y in range(3) for x in range(8)]  # 3 filas de 8 enemigos
    proyectiles = []
    disparos_enemigos = []
    puntuacion = 0

    ejecutando = True
    while ejecutando:
        pantalla.fill(BLANCO)

        # Comprobamos los eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            if evento.type == pygame.KEYDOWN:
                # Disparar proyectil con la tecla espacio
                if evento.key == pygame.K_SPACE:
                    proyectiles.append(Proyectil(nave.rect.centerx, nave.rect.top, direccion=-1))

        # Mover la nave
        teclas = pygame.key.get_pressed()
        nave.mover(teclas)

        # Mover los aliens
        for alien in aliens:
            alien.mover()
            alien.dibujar()

        # Mover los proyectiles de los aliens
        for disparo in disparos_enemigos[:]:
            disparo.mover()
            disparo.dibujar()

            # Eliminar los disparos de los aliens si salen de la pantalla
            if disparo.rect.top > ALTO:
                disparos_enemigos.remove(disparo)

        # Mover los proyectiles del jugador
        for proyectil in proyectiles[:]:
            proyectil.mover()
            proyectil.dibujar()

            # Comprobar colisiones con los aliens
            for alien in aliens[:]:
                if proyectil.rect.colliderect(alien.rect):
                    aliens.remove(alien)  # Eliminar el alien
                    proyectiles.remove(proyectil)  # Eliminar el proyectil
                    puntuacion += 1
                    break

            # Eliminar los proyectiles si salen de la pantalla
            if proyectil.rect.bottom < 0:
                proyectiles.remove(proyectil)

        # Disparo de los aliens
        if random.random() < 0.001:  # Probabilidad de que un alien dispare
            alien_disparo = random.choice(aliens)
            disparos_enemigos.append(alien_disparo.disparar())

        # Comprobar si algún alien ha llegado al fondo
        for alien in aliens:
            if alien.rect.bottom >= ALTO:
                ejecutando = False

        # Dibujar la nave
        nave.dibujar()

        # Mostrar puntuación
        fuente = pygame.font.Font(None, 36)
        puntuacion_texto = fuente.render(f"Puntuación: {puntuacion}", True, BLANCO)
        pantalla.blit(puntuacion_texto, (10, 10))

        # Actualizar la pantalla
        pygame.display.update()

        # Control de la velocidad de la actualización
        reloj.tick(60)

# Función principal
def main():
    while True:
        seleccion = pantalla_inicio()
        if seleccion == 'play':
            juego()
        elif seleccion == 'score':
            # Aquí puedes agregar una pantalla de puntajes (no implementada aún)
            print("Mostrar puntajes")
            continue

# Llamar a la función principal
main()

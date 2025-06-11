import pygame
import math
import colorsys
from random import randint, random
from ball_trail import BallTrail
from sound_manager import SoundManager
from config import (BALL_RADIUS,
                    GRAVITY,
                    WIDTH,
                    HEIGHT,
                    POS_SPAWN_BALL_Y,
                    POS_SPAWN_BALL_X_RANGE,
                    MIN_SPEED, REDUCE_SIZE_SCREEN)

LENGHT_TRAIL = 600

class Ball:
    def __init__(self):
        self.x = WIDTH // 2 + randint(-POS_SPAWN_BALL_X_RANGE, POS_SPAWN_BALL_X_RANGE)
        self.y = POS_SPAWN_BALL_Y
        self.vx = 0
        self.vy = 0
        self.radius = BALL_RADIUS
        self.sound_manager = SoundManager()

        #choix de la couleur
        self.color = (255, 0, 0)
        self.hue = random()  # valeur initiale aléatoire entre 0 et 1

        self.trail = []
        for i in range(LENGHT_TRAIL):
            self.trail.append(BallTrail(self.x, self.y, self.radius, self.color))

    def circle_colligions(self, circle):
        dx = self.x - circle.x
        dy = self.y - circle.y
        dist = math.hypot(dx, dy)

        if dist + self.radius > circle.radius and dist != 0:
            self.sound_manager.note()
            # Grossir la balle
            self.radius += 1

            # Répulsion
            nx = dx / dist
            ny = dy / dist
            penetration = dist + self.radius - circle.radius
            self.x -= nx * penetration
            self.y -= ny * penetration

            # Rebond
            dot = self.vx * nx + self.vy * ny
            self.vx -= 2 * dot * nx + 0.23 // REDUCE_SIZE_SCREEN
            self.vy -= 2 * dot * ny + 0.23 // REDUCE_SIZE_SCREEN

            # Boost de Rebond si la ball est en bas du circle
            if self.y > HEIGHT / 1.7 and math.hypot(self.vx, self.vy) < MIN_SPEED:
                add_speed = randint(5 // REDUCE_SIZE_SCREEN, 6 // REDUCE_SIZE_SCREEN)
                self.vx -= add_speed
                self.vy -= add_speed


    def update(self, circle):
        if self.y < HEIGHT + 20: #vérification sa la balle est sur l'écran
            # Gravité
            self.vy += GRAVITY

            # Déplacement
            self.x += self.vx
            self.y += self.vy

            self.circle_colligions(circle)

            # Changement couleur
            # Incrémente doucement la teinte (entre 0 et 1)
            self.hue += 0.005
            if self.hue > 1:
                self.hue -= 1  # boucle infinie

            # Convertit HSV -> RGB (valeurs entre 0 et 1)
            r, g, b = colorsys.hsv_to_rgb(self.hue, 1, 1)

            # Convertit en 0–255 pour Pygame
            self.color = (int(r * 255), int(g * 255), int(b * 255))

            # Traînée
            self.trail.pop(0)
            self.trail.append(BallTrail(self.x, self.y, self.radius, self.color))

            # Note joué
            self.sound_manager.update()

    def draw(self, screen):
        for i in range(LENGHT_TRAIL):
            self.trail[i].draw(screen, 250 - (250 / LENGHT_TRAIL * (LENGHT_TRAIL - i)))

        # Dessin du cercle principal
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
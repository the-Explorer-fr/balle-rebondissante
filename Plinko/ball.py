import pygame
import math
from random import randint, choice
from config import (BALL_RADIUS,
                    GRAVITY,
                    WIDTH,
                    PEG_RADIUS,
                    HEIGHT,
                    BALL_SPEED_MAX,
                    REDUCE_SIZE_SCREEN,
                    BALL_SPEED_MIN_X,
                    BALL_LIMIT_DRAW)

VAL_DX_BUG = 0.9 / REDUCE_SIZE_SCREEN
VAL_VX_BUG = 0.6 / REDUCE_SIZE_SCREEN

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.radius = BALL_RADIUS
        #choix de la couleur
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)

        if r < 50 and g < 50 and b < 50:
            # Choisir une composante au hasard et lui ajouter de la lumière
            channel = choice(['r', 'g', 'b'])
            if channel == 'r':
                r = randint(150, 255)
            elif channel == 'g':
                g = randint(150, 255)
            else:
                b = randint(150, 255)

        self.color = (r, g, b)

    def pegs_colligions(self, pegs):
        for peg in pegs:
            dx = self.x - peg.x
            dy = self.y - peg.y
            dist = math.hypot(dx, dy)
            min_dist = self.radius + PEG_RADIUS

            if dist < min_dist and dist != 0:
                # vérification dx non null afin d'éviter un bloquage sur le peg
                if BALL_SPEED_MIN_X > self.vx > BALL_SPEED_MIN_X * (-1):
                    if self.vx < 0:
                        self.vx = BALL_SPEED_MIN_X * (-1)
                    else:
                        self.vx = BALL_SPEED_MIN_X

                if VAL_DX_BUG * (-1) < dx < 0.3:
                    dx = 3
                    if randint(0, 1):
                        dx = -dx

                # Répulsion
                overlap = min_dist - dist
                nx = dx / dist
                ny = dy / dist
                self.x += nx * overlap
                self.y += ny * overlap

                # Rebond
                dot = self.vx * nx + self.vy * ny
                self.vx -= 2 * dot * nx
                self.vy -= 2 * dot * ny

                # Amortir légèrement
                self.vx *= 0.4
                self.vy *= 0.4


    def update(self, pegs):
        if self.y < HEIGHT + 20: #vérification sa la balle est sur l'écran
            # Gravité
            self.vy += GRAVITY

            # Déplacement
            self.x += self.vx
            self.y += self.vy

            # Collision avec les bords
            if self.x - self.radius < 0 or self.x + self.radius > WIDTH:
                self.vx *= -0.6  # Inverser la vitesse et amortir
                self.x = max(self.radius, min(WIDTH - self.radius, self.x))

            self.pegs_colligions(pegs)

            #test limite de vitesse
            if self.vx > BALL_SPEED_MAX:
                self.vx = BALL_SPEED_MAX
            elif self.vx < BALL_SPEED_MAX * (-1):
                self.vx = BALL_SPEED_MAX * (-1)


    def draw(self, screen):
        if self.y < BALL_LIMIT_DRAW:  # vérification sa la balle est sur l'écran
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

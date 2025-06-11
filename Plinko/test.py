import pygame
import math
import random

pygame.init()

WIDTH, HEIGHT = 800, 800
CENTER = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Cercle:
    def __init__(self, rayon, angle_trou=60, rotation_speed=1):
        self.rayon = rayon
        self.angle_trou = angle_trou  # En degrés
        self.angle_rotation = 0
        self.rotation_speed = rotation_speed

    def update(self):
        self.angle_rotation = (self.angle_rotation + self.rotation_speed) % 360

    def draw(self, surface):
        start_angle = math.radians(self.angle_rotation + self.angle_trou)
        end_angle = math.radians(self.angle_rotation + 360 - self.angle_trou)

        # Dessiner un arc, le cercle sauf le "trou"
        pygame.draw.arc(
            surface, (255, 255, 255),
            [CENTER.x - self.rayon, CENTER.y - self.rayon, self.rayon * 2, self.rayon * 2],
            start_angle, end_angle, 5
        )

class Balle:
    def __init__(self, pos, vitesse, rayon=5):
        self.pos = pygame.Vector2(pos)
        self.vitesse = pygame.Vector2(vitesse)
        self.rayon = rayon

    def update(self, cercle):
        to_center = self.pos - CENTER
        dist = to_center.length()
        angle_relative = (math.degrees(math.atan2(to_center.y, to_center.x)) - cercle.angle_rotation) % 360

        # Rebondir si collision avec le bord sauf dans le trou
        if dist + self.rayon >= cercle.rayon:
            if not (angle_relative > 360 - cercle.angle_trou or angle_relative < cercle.angle_trou):
                normal = to_center.normalize()
                self.vitesse.reflect_ip(normal)
                # Petite correction pour éviter les collisions multiples
                self.pos -= self.vitesse * 2

        self.pos += self.vitesse

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 0, 0), (int(self.pos.x), int(self.pos.y)), self.rayon)

# Initialisation
cercle_principal = Cercle(rayon=200, angle_trou=60, rotation_speed=1)
balle = Balle(pos=(CENTER.x + 100, CENTER.y), vitesse=(3, 2))

# Boucle principale
running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    cercle_principal.update()
    balle.update(cercle_principal)

    cercle_principal.draw(screen)
    balle.draw(screen)

    # Cercles supplémentaires (infini simulé)
    for i in range(1, 5):
        rayon_extra = cercle_principal.rayon + i * 50
        pygame.draw.circle(screen, (50, 50, 50), CENTER, rayon_extra, 1)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

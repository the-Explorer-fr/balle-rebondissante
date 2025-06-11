import pygame
from config import WIDTH, HEIGHT, BACKGROUND_COLOR, CIRCLE_BASE_RADIUS, REDUCE_SIZE_SCREEN, RESPONSES_NUMBER, \
    NUMBER_CIRCLES, HOLE_SIZE_DEGRE
import math

class Circle:
    def __init__(self, ratio):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.radius = int(CIRCLE_BASE_RADIUS) * (1 + ratio / 3.4)
        #self.speed = 1 + (2.3 * ratio / 5) / REDUCE_SIZE_SCREEN
        self.speed = 1.5
        self.speed_size = 4 / REDUCE_SIZE_SCREEN
        self.start_angle = normalize_angle(math.radians(0 - 10 * ratio))
        self.end_angle = normalize_angle(math.radians(360 - HOLE_SIZE_DEGRE - 10 * ratio))

    def update(self, ratio, reduce_size_circles):
        if reduce_size_circles:
            self.radius -= self.speed_size
        #self.speed = 1 + 1 * ratio / 75
        #voir la distance de base entre cercle 0 et 1
        self.start_angle = normalize_angle(self.start_angle - math.radians(self.speed))
        self.end_angle = normalize_angle(self.end_angle - math.radians(self.speed))

    def draw(self, screen):
        # Dessine le disque principal
        if self.radius < HEIGHT / 1.7:
            pygame.draw.circle(screen, (240, 240, 240), (self.x, self.y), self.radius, 0)

            # Dessine un triangle noir pour simuler le trou
            angle1 = self.end_angle
            angle2 = self.start_angle

            x1 = self.x + self.radius * 1.10472 * math.cos(angle1)
            y1 = self.y + self.radius * 1.10472 * math.sin(angle1)
            x2 = self.x + self.radius * 1.10472 * math.cos(angle2)
            y2 = self.y + self.radius * 1.10472 * math.sin(angle2)

            pygame.draw.polygon(screen, BACKGROUND_COLOR, [(self.x, self.y), (x1, y1), (x2, y2)])

            # Centre transparent
            pygame.draw.circle(screen, BACKGROUND_COLOR, (self.x, self.y), self.radius - 10 // REDUCE_SIZE_SCREEN)

def normalize_angle(angle):
    return angle % (2 * math.pi)
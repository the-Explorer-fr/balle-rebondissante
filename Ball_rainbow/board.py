import pygame
from config import WIDTH, HEIGHT, BACKGROUND_COLOR, CIRCLE_BASE_RADIUS

class Circle:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.radius = CIRCLE_BASE_RADIUS

    def draw(self, screen):
        pygame.draw.circle(screen, (100, 0, 100), (self.x, self.y), self.radius)
        pygame.draw.circle(screen, BACKGROUND_COLOR, (self.x, self.y), self.radius - 5)

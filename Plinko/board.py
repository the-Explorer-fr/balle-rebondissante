import pygame
from config import PEG_COLOR, PEG_RADIUS

class Peg:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.circle(screen, PEG_COLOR, (self.x, self.y), PEG_RADIUS)

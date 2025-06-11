import pygame

class BallTrail:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, screen, transparence):
        circle_trail = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)

        # Cercle coloré transparent
        pygame.draw.circle(circle_trail, (*self.color, transparence), (self.radius, self.radius), self.radius)

        # Blit sur l'écran principal
        screen.blit(circle_trail, (self.x - self.radius, self.y - self.radius))
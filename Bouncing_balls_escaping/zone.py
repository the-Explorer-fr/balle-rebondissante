import pygame

from config import HEIGHT, WIDTH, ZONE_POSITION_Y

pygame.font.init()

class ZoneDetector:
    def __init__(self, x, height, width, color, label):
        self.rect = pygame.Rect(x, HEIGHT - ZONE_POSITION_Y, width, height)
        self.color = color
        self.label = label
        self.count = 0
        self.font = pygame.font.SysFont(None, 24)

        # Surface transparente pour le fond
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        transparent_color = (*color[:3], 80)  # Ajout alpha (80 sur 255 ≈ 30%)
        self.surface.fill(transparent_color)

    def check_collision(self, ball):
        if self.rect.collidepoint(ball.x, ball.y) and not hasattr(ball, 'counted'):
            self.count += 1
            ball.counted = True  # Évite de compter plusieurs fois la même balle

    def draw(self, screen):
        # Dessine la surface transparente (fond)
        screen.blit(self.surface, (self.rect.x, self.rect.y))

        # Dessine le contour
        pygame.draw.rect(screen, self.color, self.rect, 2)

        # Texte multi-ligne avec le score
        lines = f"{self.label}\n{self.count}".split("\n")
        line_height = self.font.get_linesize()
        total_text_height = len(lines) * line_height
        start_y = self.rect.y + self.rect.height / 2 - total_text_height / 2

        for i, line in enumerate(lines):
            text_surface = self.font.render(line, True, self.color)
            text_x = self.rect.x + self.rect.width / 2 - text_surface.get_width() / 2
            text_y = start_y + i * line_height
            screen.blit(text_surface, (text_x, text_y))

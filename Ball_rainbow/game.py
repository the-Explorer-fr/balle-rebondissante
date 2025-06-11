import pygame
from config import (WIDTH,
                    HEIGHT,
                    BACKGROUND_COLOR,
                    FPS,
                    ZONES, TEXT_QUESTION,
                    TEXT_QUESTION_POS,
                    TIME_VIDEO,
                    TIME_END_VIDEO,
                    FONT)

from board import Circle
from sound_manager import SoundManager
from ball import Ball
import time

def event_gestion(running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = -1
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #balls.append(Ball(*pygame.mouse.get_pos()))
            running = 0
    return running


def update(screen, balls, circles, dt):
    screen.fill(BACKGROUND_COLOR)

    for circle in circles:
        circle.draw(screen)

    for ball in balls:
        ball.update(circles[0])
        ball.draw(screen)

    pygame.display.flip()


def run_game(record_video=False):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    time.sleep(1)

    clock = pygame.time.Clock()
    balls = []
    balls.append(Ball())
    circles = []
    circles.append(Circle())
    start_time = 0
    if record_video:
        start_time = pygame.time.get_ticks()

    running = 1

    #simulation
    while running == 1:
        running = event_gestion(running)

        if record_video:
            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
            if elapsed_time >= TIME_VIDEO:
                running = False


        dt = clock.tick(FPS) / 1000

        update(screen, balls, circles, dt)
        
    """
    #End simulation
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    max_count = max(zone.count for zone in ZONES)
    winning_zones = [zone for zone in ZONES if zone.count == max_count]
    if running != -1:
        running = 2

    while running:

        dt = clock.tick(FPS) / 1000

        update(screen, balls, circles, dt)

        # Highlight zone winner
        for zone in winning_zones:
            pygame.draw.rect(screen, zone.color, zone.rect.inflate(20, 20), 5)

        for zone in winning_zones:
            label_surface = FONT.render(f"WINER : {zone.label}", True, zone.color)
            pygame.draw.rect(screen, (0, 0, 0),
                [WIDTH / 2 - (label_surface.get_width() + (label_surface.get_width() // 2)) / 2,
                 HEIGHT / 2 - (label_surface.get_height() + label_surface.get_height()) / 2,
                 label_surface.get_width() + (label_surface.get_width() // 2),
                 label_surface.get_height() + label_surface.get_height()])
            screen.blit(label_surface, (
                WIDTH / 2 - label_surface.get_width() / 2,
                HEIGHT / 2 - label_surface.get_height() / 2
            ))


        pygame.display.flip()

        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000

        event_gestion(running)

        if elapsed_time >= TIME_END_VIDEO:
            running = False
        """
    pygame.quit()
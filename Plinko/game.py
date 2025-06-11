import pygame
from config import (WIDTH,
                    HEIGHT,
                    BACKGROUND_COLOR,
                    FPS,
                    SPACING_WIDTH_PEGS,
                    SPACING_HEIGHT_PEGS,
                    PEGS_POSITION_Y,
                    ZONES, TEXT_QUESTION,
                    TEXT_QUESTION_POS,
                    TIME_VIDEO,
                    TIME_END_VIDEO,
                    FONT,
                    NB_PEGS_LINE, REDUCE_SIZE_SCREEN, MARGIN)

from board import Peg
from spawner import Spawner
from sound_manager import SoundManager
import time

def pegs_generate_recursive(pos, pegs, nb_pegs, end):
    if end == 0:
        return pegs
    if nb_pegs % 2 == 1:
        pegs.append(Peg(pos[0], pos[1]))
        for i in range(1, nb_pegs // 2 + 1):
            pegs.append(Peg(pos[0] + SPACING_WIDTH_PEGS * i, pos[1]))
            pegs.append(Peg(pos[0] - SPACING_WIDTH_PEGS * i, pos[1]))
    else:
        for i in range(nb_pegs // 2):
            offset = SPACING_WIDTH_PEGS * i + SPACING_WIDTH_PEGS // 2
            pegs.append(Peg(pos[0] + offset, pos[1]))
            pegs.append(Peg(pos[0] - offset, pos[1]))
    return pegs_generate_recursive([pos[0], pos[1] + SPACING_HEIGHT_PEGS], pegs, nb_pegs + 1, end - 1)


def pegs_setup():
    return pegs_generate_recursive([WIDTH / 2, PEGS_POSITION_Y], [], 3, NB_PEGS_LINE)


def event_gestion(running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = -1
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #balls.append(Ball(*pygame.mouse.get_pos()))
            running = 0
    return running


def update(screen, pegs, balls, spawner, sound_manager, dt, running):
    screen.fill(BACKGROUND_COLOR)
    spawner.update(dt, balls, sound_manager)
    for peg in pegs:
        peg.draw(screen)

    for ball in balls:
        ball.update(pegs)
        if running == 1:
            for zone in ZONES:
                zone.check_collision(ball)
        ball.draw(screen)

    for zone in ZONES:
        zone.draw(screen)

    spawner.draw(screen)

    #affichage question
    pygame.draw.rect(screen,
                (255, 255, 255),
                     pygame.Rect(TEXT_QUESTION_POS[0] - MARGIN,
                                 TEXT_QUESTION_POS[1] - MARGIN,
                                 TEXT_QUESTION.get_width() + 2 * MARGIN,
                                 TEXT_QUESTION.get_height() + 2 * MARGIN))
    screen.blit(TEXT_QUESTION, TEXT_QUESTION_POS)

    pygame.display.flip()


def score_not_equal():
    for i in range(len(ZONES)):
        for j in range(len(ZONES)):
            if i != j:
                if ZONES[i].count == ZONES[j].count:
                    return False
    return True

def print_winner_zone(screen, winner_zone):
    pygame.draw.rect(screen, winner_zone.color, winner_zone.rect.inflate(20, 20), 5)

    label_surface = FONT.render(f"WINER : {winner_zone.label}", True, winner_zone.color)
    pygame.draw.rect(screen, (0, 0, 0),
                     [WIDTH / 2 - (label_surface.get_width() + (label_surface.get_width() // 2)) / 2,
                      HEIGHT / 2 - (label_surface.get_height() + label_surface.get_height()) / 2,
                      label_surface.get_width() + (label_surface.get_width() // 2),
                      label_surface.get_height() + label_surface.get_height()])
    screen.blit(label_surface, (
        WIDTH / 2 - label_surface.get_width() / 2,
        HEIGHT / 2 - label_surface.get_height() / 2
    ))

def run_game(record_video=False):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    time.sleep(1)

    clock = pygame.time.Clock()
    balls = []
    pegs = pegs_setup()
    spawner = Spawner()
    sound_manager = SoundManager()
    start_time = 0
    if record_video:
        start_time = pygame.time.get_ticks()

    sound_manager.play_music()

    running = 1

    """     simulation     """
    while running == 1:
        running = event_gestion(running)

        if record_video:
            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
            if elapsed_time >= TIME_VIDEO and score_not_equal():
                running = False


        dt = clock.tick(FPS) / 1000

        update(screen, pegs, balls, spawner, sound_manager, dt, running)
        

    """     End simulation     """
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()

    winner_score = max(ZONES[i].count for i in range(len(ZONES)))
    winner_zone = None
    for zone in ZONES:
        if zone.count == winner_score:
            winner_zone = zone
            break

    if running != -1:
        running = 2
    sound_manager.play_validation()

    while running:

        dt = clock.tick(FPS) / 1000

        update(screen, pegs, balls, spawner, sound_manager, dt, running)

        # Highlight zone winner
        print_winner_zone(screen, winner_zone)

        pygame.display.flip()

        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000

        event_gestion(running)

        if elapsed_time >= TIME_END_VIDEO:
            running = False

    pygame.quit()
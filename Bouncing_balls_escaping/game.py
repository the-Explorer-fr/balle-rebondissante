import pygame
from config import (WIDTH,
                    HEIGHT,
                    BACKGROUND_COLOR,
                    FPS,
                    TEXT_QUESTION,
                    TEXT_QUESTION_POS,
                    TIME_VIDEO,
                    TIME_END_VIDEO,
                    FONT,
                    NUMBER_CIRCLES,
                    RESPONSES_NUMBER,
                    CIRCLE_MIN_SIZE,
                    COLOR_LIST,
                    RESPONSES_LIST,
                    ZONE_WIDTH,
                    REDUCE_SIZE_SCREEN,
                    TEXT_WINNER_POS,
                    WINNER_SIZE,
                    WINNER_FONT,
                    LITTLE_FONT,
                    TEXT_TIMER_POS_Y)

from circle import Circle
from sound_manager import SoundManager
from ball import Ball
from particles import Particles
from sound_manager import SoundManager
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

def print_question(screen):
    text_x, text_y = TEXT_QUESTION_POS

    # Ajouter une marge autour du texte
    padding = 25 / REDUCE_SIZE_SCREEN
    rect_width = TEXT_QUESTION.get_width() + 2 * padding
    rect_height = TEXT_QUESTION.get_height() + 2 * padding

    rect = pygame.Rect(text_x, text_y, rect_width, rect_height)

    # Dessin du fond blanc
    pygame.draw.rect(screen, (255, 255, 255), rect)

    # Affichage du texte centré dans le rectangle
    screen.blit(TEXT_QUESTION, (text_x + padding, text_y + padding))

def print_winner(screen, text, score, color):
    text_x, text_y = TEXT_WINNER_POS

    rect_width = WINNER_SIZE[0]
    rect_height = WINNER_SIZE[1]

    rect = pygame.Rect(text_x - rect_width / 2, text_y - rect_height / 2, rect_width, rect_height)

    # Dessin du fond blanc
    pygame.draw.rect(screen, (255, 255, 255), rect)

    # Texte multi-ligne avec le score
    lines = f'WINNER !\n"{text}"\nScore : {score}'.split("\n")
    line_height = FONT.get_linesize() + 20 / REDUCE_SIZE_SCREEN
    total_text_height = len(lines) * line_height
    start_y = rect.y + rect.height / 2 - total_text_height / 2

    for i, line in enumerate(lines):
        text_surface = WINNER_FONT.render(line, True, color)
        text_x = rect.x + rect.width / 2 - text_surface.get_width() / 2
        text_y = start_y + i * line_height
        screen.blit(text_surface, (text_x, text_y))

def update(screen, balls, circles, list_particles, circles_removed, sound_manager, reduce_size_circles, running):
    screen.fill(BACKGROUND_COLOR)

    for i in range(NUMBER_CIRCLES - 1 - circles_removed, -1, -1):
        circles[i].update(i, reduce_size_circles)
        circles[i].draw(screen)

    if circles[0].radius < CIRCLE_MIN_SIZE:
        reduce_size_circles = False

    pos_zone_x_rl = -1
    for i in range(len(balls)):
        bounce = balls[i].update(circles[0], running, reduce_size_circles)
        balls[i].draw(screen)

        if not bounce:
            sound_manager.play_destroy_circle()
            circles_removed += 1
            list_particles.append(Particles(circles[0].radius, circles[0].x, circles[0].y, circles[0].start_angle, circles[0].end_angle))
            circles.remove(circles[0])
            reduce_size_circles = True

        if bounce == 2:
            sound_manager.note()

        for j in range(len(balls)):
            if j != i:
                bounce = balls[i].ball_colligions(balls[j])
                if bounce:
                    sound_manager.note()

        for particles in list_particles:
            if particles.length() == 0:
                list_particles.remove(particles)
            else:
                particles.update(screen)

    #afficher les réponses
    for i, ball in enumerate(balls):
        x_zone = WIDTH / 2 + (i - len(balls) / 2) * (ZONE_WIDTH + 10)
        ball.draw_zone(screen, x_zone)

    print_question(screen)

    sound_manager.update()
    return circles_removed, reduce_size_circles


def score_not_equal(balls):
    for i in range(len(balls)):
        for j in range(len(balls)):
            if i != j:
                if balls[i].score == balls[j].score:
                    return False
    return True


def draw_timer(screen, timer):
    text_time = FONT.render(f"{str(timer // 60)} : {str(timer % 60).zfill(2)}", True, (0, 0, 0))
    text_x, text_y = WIDTH / 2 - text_time.get_width() / 2, TEXT_TIMER_POS_Y

    padding = 25 / REDUCE_SIZE_SCREEN
    rect_width = text_time.get_width() + 2 * padding
    rect_height = text_time.get_height() + 2 * padding

    rect = pygame.Rect(text_x - padding, text_y - padding, rect_width, rect_height)

    # Fond blanc
    pygame.draw.rect(screen, (255, 255, 255), rect)

    # Dessin du texte
    screen.blit(text_time, (text_x, text_y))


def run_game(record_video=False):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    sound_manager = SoundManager()

    time.sleep(1)

    reduce_size_circles = True
    circles_removed = 0
    clock = pygame.time.Clock()
    time_second = TIME_VIDEO
    balls = []
    for i in range(RESPONSES_NUMBER):
        balls.append(Ball(COLOR_LIST[i], RESPONSES_LIST[i]))
    circles = []
    for i in range (NUMBER_CIRCLES):
        circles.append(Circle(i))
    #circles.append(Circle(0))
    list_particles = []

    start_time = 0
    if record_video:
        start_time = pygame.time.get_ticks()

    running = 1

    """     simulation     """
    while running:
        running = event_gestion(running)

        circles_removed, reduce_size_circles = update(screen,
                                                      balls,
                                                      circles,
                                                      list_particles,
                                                      circles_removed,
                                                      sound_manager,
                                                      reduce_size_circles,
                                                      running)

        if record_video:
            draw_timer(screen, time_second)
            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
            if TIME_VIDEO - elapsed_time < time_second and time_second > 0:
                time_second -= 1
            if elapsed_time >= TIME_VIDEO and score_not_equal(balls):
                running = 0

        pygame.display.flip()
        clock.tick(FPS)


    """     End simulation     """
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    running = 2

    winner_score = max(balls[i].score for i in range(RESPONSES_NUMBER))
    winner_ball = None
    for ball in balls:
        if ball.score == winner_score:
            winner_ball = ball
            break

    text, score, color = winner_ball.text, winner_ball.score, winner_ball.color

    sound_manager.play_validation()

    while running:

        circles_removed, reduce_size_circles = update(screen, balls, circles, list_particles, circles_removed, sound_manager, reduce_size_circles, running)
        print_winner(screen, text, score, color)

        pygame.display.flip()

        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000

        event_gestion(running)

        if elapsed_time >= TIME_END_VIDEO:
            running = False

        clock.tick(FPS)

    pygame.quit()
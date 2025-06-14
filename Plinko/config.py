REDUCE_SIZE_SCREEN = 1.9

"""         SCREEN MANAGEMENT         """
WIDTH, HEIGHT = 1080 // REDUCE_SIZE_SCREEN, 1920 // REDUCE_SIZE_SCREEN
BACKGROUND_COLOR = (30, 30, 30)

"""         TIME MANAGEMENT         """
FPS = 70
TIME_VIDEO = 57 #seconds
TIME_END_VIDEO = 5 #seconds

"""         PEG MANAGEMENT         """
NB_PEGS_LINE = 13
PEG_RADIUS = 10 // REDUCE_SIZE_SCREEN
PEG_COLOR = (200, 200, 200)
PEGS_POSITION_Y = HEIGHT / 3.8
SPACING_WIDTH_PEGS = 15 * PEG_RADIUS // REDUCE_SIZE_SCREEN
SPACING_HEIGHT_PEGS = 15 * PEG_RADIUS // REDUCE_SIZE_SCREEN

"""         BALL MANAGEMENT         """
GRAVITY = 0.8 / REDUCE_SIZE_SCREEN
BALL_RADIUS = 17 // REDUCE_SIZE_SCREEN
BALL_SPEED_MAX = 4 / REDUCE_SIZE_SCREEN
BALL_SPEED_MIN_X = BALL_SPEED_MAX / 1.3

"""         SPAWNER MANAGEMENT         """
POSITION_Y_SPAWNER = 370 // REDUCE_SIZE_SCREEN
TIME_SPAWN_MIN = 0.05
TIME_SPAWN_MAX = 0.2
SPAWNER_WIDTH = 50 / REDUCE_SIZE_SCREEN
SPAWNER_HEIGHT = 45 / REDUCE_SIZE_SCREEN

"""         ZONE ANSWERS MANAGEMENT         """
#HEIGHT - ZONE_POSITION_Y = position on screen
ZONE_POSITION_Y = 300 // REDUCE_SIZE_SCREEN
BALL_LIMIT_DRAW = HEIGHT - ZONE_POSITION_Y + BALL_RADIUS * 2

COLOR_LIST = [(0, 255, 0), (255, 0, 0), (100, 87, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

"""         QUESTION AND ANSWERS MANAGEMENT         """
import pygame
pygame.init()
QUESTION = "ça va ?"

# FONT TEXT
FONT = pygame.font.SysFont(None, 42)
TEXT_QUESTION = FONT.render(QUESTION, True, (0, 0, 0))
TEXT_QUESTION_POSITION_Y = 190 // REDUCE_SIZE_SCREEN
TEXT_QUESTION_POS = (WIDTH / 2 - TEXT_QUESTION.get_width() / 2, TEXT_QUESTION_POSITION_Y)
#Bloc de couleur derrière le texte de la question marge
MARGIN = 20 // REDUCE_SIZE_SCREEN

RESPONSES_NUMBER = 2
RESPONSE_1 = "Yes"
RESPONSE_2 = "No"
RESPONSES_LIST = [RESPONSE_1, RESPONSE_2]

from zone import ZoneDetector
zone_width = WIDTH // RESPONSES_NUMBER
zone_height = ZONE_POSITION_Y / 2
ZONES = []
for i in range(RESPONSES_NUMBER):
    ZONES.append(ZoneDetector(0 + i * zone_width, zone_height, zone_width, COLOR_LIST[i], RESPONSES_LIST[i]))
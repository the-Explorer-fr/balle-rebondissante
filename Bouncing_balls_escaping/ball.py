import pygame
import math
from random import randint, random, uniform
from ball_trail import BallTrail
from config import (BALL_RADIUS,
                    GRAVITY,
                    WIDTH,
                    HEIGHT,
                    POS_SPAWN_BALL_Y,
                    POS_SPAWN_BALL_X_RANGE,
                    REDUCE_SIZE_SCREEN,
                    ZONE_WIDTH,
                    ZONE_HEIGHT,
                    ZONE_POSITION_Y,
                    FONT,
                    LITTLE_FONT,
                    BALL_MIN_SPEED)

LENGHT_TRAIL = 13

class Ball:
    def __init__(self, color, text):
        self.x = WIDTH // 2 + randint(-POS_SPAWN_BALL_X_RANGE, POS_SPAWN_BALL_X_RANGE)
        self.y = POS_SPAWN_BALL_Y
        self.vx = 0
        self.vy = 0
        self.radius = BALL_RADIUS
        self.color = color
        self.trail = [BallTrail(self.x, self.y, self.radius, self.color) for i in range(LENGHT_TRAIL)]
        self.is_in = True
        self.score = 0
        self.text = text

    def circle_colligions(self, circle, running, reduce_size_circles):
        dx = self.x - circle.x
        dy = self.y - circle.y
        dist = math.hypot(dx, dy)

        # Rebond si touche bord écran
        if self.x + self.radius > WIDTH or self.x - self.radius < 0:
            self.vx = -self.vx
            return 2
        if self.y + self.radius > HEIGHT or self.y - self.radius < 0:
            self.vy = -self.vy
            return 2

        if dist + self.radius > circle.radius and dist != 0:
            if is_ball_in_arc(dx, dy, circle.start_angle, circle.end_angle):

                # Normal du contact
                nx = dx / dist
                ny = dy / dist

                # Corriger la position
                penetration = dist + self.radius - circle.radius
                self.x -= nx * penetration * 3
                self.y -= ny * penetration * 3

                # Rebond
                if reduce_size_circles:
                    dot = self.vx * nx + self.vy * ny + circle.speed_size
                else:
                    dot = self.vx * nx + self.vy * ny
                self.vx -= 2 * dot * nx
                self.vy -= 2 * dot * ny

                speed = math.hypot(self.vx, self.vy)
                if speed < 2 * circle.speed_size and reduce_size_circles:
                    self.vx -= nx * 10 // REDUCE_SIZE_SCREEN
                    self.vy -= ny * 10 // REDUCE_SIZE_SCREEN
                """
                # Boost de Rebond si la ball est en bas du circle
                if self.y > HEIGHT / 1.7 and math.hypot(self.vx, self.vy) < BALL_MIN_SPEED:
                    add_speed = randint(6 // REDUCE_SIZE_SCREEN, 7 // REDUCE_SIZE_SCREEN)
                    self.vx -= nx * add_speed
                    self.vy -= ny * add_speed
                """

                # Limite de vitesse maximale
                max_speed = 25 // REDUCE_SIZE_SCREEN
                speed = math.hypot(self.vx, self.vy)

                if speed > max_speed:
                    scale = max_speed / speed
                    self.vx *= scale
                    self.vy *= scale
                return 2

            else:
                if running == 1:
                    self.score += 1
                return 0
        return 1

    def ball_colligions(self, ball):
        dx = self.x - ball.x
        dy = self.y - ball.y
        dist = math.hypot(dx, dy)
        min_dist = self.radius + ball.radius

        if dist < min_dist and dist != 0:
            nx = dx / dist
            ny = dy / dist

            # Correction de position
            penetration = (min_dist - dist) / 2
            self.x += nx * penetration
            self.y += ny * penetration
            ball.x -= nx * penetration
            ball.y -= ny * penetration

            # Vitesse relative
            rvx = self.vx - ball.vx
            rvy = self.vy - ball.vy

            # Vitesse projetée sur la normale
            dot = rvx * nx + rvy * ny

            # Si les balles s'éloignent, pas de rebond
            if dot > 0:
                return False

            # Impulsion élastique (masse = 1)
            impulse = 2 * dot / 2
            self.vx -= impulse * nx
            self.vy -= impulse * ny
            ball.vx += impulse * nx
            ball.vy += impulse * ny
            if self.vy == ball.vy:
                ball.vx += 2
                return False

            return True
        return False


    def update(self, circle, running, reduce_size_circles):
        self.vy += GRAVITY
        self.x += self.vx
        self.y += self.vy
        bounce = self.circle_colligions(circle, running, reduce_size_circles)
        self.trail.pop(0)
        self.trail.append(BallTrail(self.x, self.y, self.radius, self.color))
        return bounce


    def draw(self, screen):
        for i in range(LENGHT_TRAIL):
            self.trail[i].draw(screen, 250 - (250 / LENGHT_TRAIL * (LENGHT_TRAIL - i)))
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y)), self.radius * 0.9)
        text_surface = LITTLE_FONT.render(self.text, True, (255, 255, 255))
        text_x = self.x - text_surface.get_width() / 2
        text_y = self.y - text_surface.get_height() / 2
        screen.blit(text_surface, (text_x, text_y))

    def draw_zone(self, screen, x):
        rect = pygame.Rect(x, ZONE_POSITION_Y, ZONE_WIDTH, ZONE_HEIGHT)
        pygame.draw.rect(screen, (255, 255, 255), rect)

        # Texte multi-ligne avec le score
        lines = f"{self.text}\n{self.score}".split("\n")
        text_surfaces = [FONT.render(line, True, self.color) for line in lines]
        total_text_height = sum(surface.get_height() for surface in text_surfaces)

        start_y = rect.y + rect.height / 2 - total_text_height / 2

        for surface in text_surfaces:
            text_x = rect.x + rect.width / 2 - surface.get_width() / 2
            screen.blit(surface, (text_x, start_y))
            start_y += surface.get_height()


def is_ball_in_arc(dx, dy, start_angle, end_angle):
    angle_ball = normalize_angle(math.atan2(dy, dx))
    """
    # Marge de sécurité (demi-angle de la balle projetée sur le cercle)
    #margin = 0.06
    # Réduction de l'ouverture virtuelle (pour éviter les erreurs de bord)
    #start = normalize_angle(start_angle - margin)
    #end = normalize_angle(end_angle + margin)
    """
    start = normalize_angle(start_angle)
    end = normalize_angle(end_angle)

    # Gestion des cas où l'arc traverse 0 radians
    if start < end:
        return start <= angle_ball <= end
    else:
        return angle_ball >= start or angle_ball <= end

def normalize_angle(angle):
    return angle % (2 * math.pi)
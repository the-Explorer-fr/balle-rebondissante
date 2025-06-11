import pygame
import random
import time
from config import (WIDTH,
                    SPACING_WIDTH_PEGS,
                    REDUCE_SIZE_SCREEN,
                    TIME_SPAWN_MIN,
                    TIME_SPAWN_MAX,
                    POSITION_Y_SPAWNER)
from ball import Ball

class Spawner:
    def __init__(self):
        self.width = 35 / REDUCE_SIZE_SCREEN
        self.height = 30 / REDUCE_SIZE_SCREEN
        self.y = POSITION_Y_SPAWNER
        self.x = WIDTH // 2 - self.width // 2
        self.vx = random.uniform(80, 150) * random.choice([-1, 1])
        self.ax = 0
        self.max_speed = abs(self.vx)
        self.last_spawn = time.time()
        self.next_delay = random.uniform(0.1, 0.3)

    def update(self, dt, ball_list, sound_manager=None):
        if self.x < WIDTH // 2 - SPACING_WIDTH_PEGS * 2:
            self.ax = 500
        elif self.x + self.width > WIDTH // 2 + SPACING_WIDTH_PEGS * 2:
            self.ax = -500
        else:
            self.ax = 0

        self.vx += self.ax * dt
        self.vx = max(-self.max_speed, min(self.vx, self.max_speed))
        self.x += self.vx * dt

        current_time = time.time()
        if current_time - self.last_spawn >= self.next_delay:
            ball_x = self.x + self.width // 2
            ball_list.append(Ball(ball_x, self.y + self.height))
            self.last_spawn = current_time
            self.next_delay = random.uniform(TIME_SPAWN_MIN, TIME_SPAWN_MAX)

            if sound_manager is not None:
                sound_manager.play_spawn()

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 165, 0), (int(self.x), self.y, self.width, self.height))
        #pygame.draw.circle(screen, (255, 165, 0), (int(self.x), int(self.y)), self.width)

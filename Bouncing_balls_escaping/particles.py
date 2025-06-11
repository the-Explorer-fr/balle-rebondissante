import pygame
import math
from random import randint, random, uniform
import time
import math

from config import NUMBER_PARTICLES, HOLE_SIZE_DEGRE


class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = uniform(-1, 1)
        self.vy = uniform(-1, 1)
        self.radius = uniform(0.8, 1.7)
        self.time_live = uniform(0.2, 0.6)

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def is_in_live(self, time_created, time_now):
        return self.time_live > time_now - time_created

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.radius)

class Particles:
    """
    def __init__(self, radius, center_x, center_y, angle_start_hole, angle_end_hole):
        self.time_created = time.time()
        print(self.time_created)
        self.particles = []
        ratio_angle_particule = (math.radians(360) - HOLE_SIZE_DEGRE) / NUMBER_PARTICLES
        for i in range(NUMBER_PARTICLES):
            self.particles.append(Particle(center_x + radius * math.cos(angle_start_hole + ratio_angle_particule * i),
                                           center_y + radius * math.sin(angle_start_hole + ratio_angle_particule * i)))
    """

    def __init__(self, radius, center_x, center_y, angle_end_hole, angle_start_hole):
        self.time_created = time.time()
        self.particles = []

        # Normalise les angles (utile si end < start)
        angle_start_hole = angle_start_hole % (2 * math.pi)
        angle_end_hole = angle_end_hole % (2 * math.pi)

        # Détermine les segments d’angles disponibles
        angle_ranges = []
        if angle_end_hole > angle_start_hole:
            # Trou ne chevauche pas 0 radian
            angle_ranges.append((0, angle_start_hole))
            angle_ranges.append((angle_end_hole, 2 * math.pi))
        else:
            # Trou chevauche 0 radian
            angle_ranges.append((angle_end_hole, angle_start_hole))

        # Calcul du total d’angle disponible
        total_angle = sum(end - start for start, end in angle_ranges)

        # Génère les angles des particules uniquement en dehors du trou
        angle = 0
        for _ in range(NUMBER_PARTICLES):
            r = random() * total_angle
            acc = 0
            for start, end in angle_ranges:
                if acc + (end - start) >= r:
                    angle = start + (r - acc)
                    break
                acc += end - start

            # Création de la particule
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            self.particles.append(Particle(x, y))

    def update(self, screen):
        time_now = time.time()
        for particle in self.particles:
            if particle.is_in_live(self.time_created, time_now):
                particle.update()
                particle.draw(screen)
            else:
                self.particles.remove(particle)

    def length(self):
        return len(self.particles)
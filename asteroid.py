import random

import pygame

from circleshape import CircleShape
from constants import *


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self, weapon="default"):
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS or weapon == "rocket":
            return

        angle = random.uniform(10, 60)

        vector1 = self.velocity.rotate(angle) * 1.2
        vector2 = self.velocity.rotate(-angle) * 1.2

        new_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid1 = Asteroid(self.position.x + new_radius, self.position.y, new_radius)
        asteroid1.velocity = vector1
        asteroid2 = Asteroid(self.position.x, self.position.y + new_radius, new_radius)
        asteroid2.velocity = vector2

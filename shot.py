import pygame

from circleshape import CircleShape
from constants import *


class Shot(CircleShape):
    def __init__(self, x, y, weapon):
        super().__init__(x, y, SHOT_RADIUS)
        self.weapon = weapon

    def draw(self, screen):
        if self.weapon == "default":
            pygame.draw.circle(screen, "white", self.position, self.radius, 2)
        elif self.weapon == "rocket":
            pygame.draw.circle(screen, "white", self.position, self.radius * 2, 2)

    def update(self, dt):
        self.position += self.velocity * dt

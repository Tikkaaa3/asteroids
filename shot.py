import pygame

from circleshape import CircleShape
from constants import *


class Shot(CircleShape):
    cooldown = 0.5

    def __init__(self, x, y, weapon):
        super().__init__(x, y, SHOT_RADIUS)
        self.weapon = weapon

    def draw(self, screen, rocket_count):
        if self.weapon == "default":
            pygame.draw.circle(screen, "white", self.position, self.radius, 2)
            return rocket_count

        elif self.weapon == "rocket" and rocket_count > 0:
            pygame.draw.circle(screen, "white", self.position, self.radius * 2, 2)
            print(self.cooldown)
            if self.cooldown < 0:
                rocket_count -= 1
                self.cooldown = 0.5
            return rocket_count
        return rocket_count

    def update(self, dt):
        self.position += self.velocity * dt

import pygame

from circleshape import CircleShape
from constants import *
from shot import Shot


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.cooldown = PLAYER_SHOOT_COOLDOWN
        self.weapon = "default"
        self.change_cooldown = 0

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_c]:
            if self.change_cooldown < 0.0:
                print("changed")
                if self.weapon == "default":
                    self.weapon = "rocket"
                else:
                    self.weapon = "default"
                self.change_cooldown = 1
        if keys[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
        weapon = self.weapon
        if weapon == "default":
            if self.cooldown < 0.0:
                shot = Shot(self.position.x, self.position.y, weapon)
                shot.velocity = (
                    pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
                )
                self.cooldown = 0.3
        elif weapon == "rocket":
            if self.cooldown < 0.0:
                shot = Shot(self.position.x, self.position.y, weapon)
                shot.velocity = (
                    pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
                )
                self.cooldown = 0.8

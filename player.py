import pygame

from circleshape import CircleShape
from constants import *
from shot import Shot


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0  # Initial facing direction (0 radians, facing upwards)
        self.cooldown = PLAYER_SHOOT_COOLDOWN
        self.weapon = "default"
        self.change_cooldown = 0

        # Acceleration and movement variables
        self.velocity = pygame.Vector2(0, 0)  # Initial velocity is zero
        self.acceleration = PLAYER_ACCELERATION
        self.max_speed = PLAYER_MAX_SPEED
        self.deceleration = PLAYER_DECELERATION
        self.rotation_velocity = 0  # Rotation speed (affects how fast the player turns)
        self.last_movement = None  # Track last movement direction
        self.is_moving = False  # Track if the player is moving

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
        # Apply the rotation velocity smoothly
        self.rotation += self.rotation_velocity * dt

    def move(self, dt, forward: bool):
        # Calculate forward velocity vector based on the player's rotation
        direction = pygame.Vector2(0, 1).rotate(self.rotation)

        # If we change direction (e.g., from W to S or S to W), reset velocity but keep rotation
        if self.last_movement != forward:
            self.velocity = pygame.Vector2(0, 0)  # Reset velocity on direction change
            self.rotation_velocity = 0  # Reset rotation velocity on direction change

        if forward:
            self.velocity += direction * self.acceleration * dt  # Accelerate forward
        else:
            self.velocity -= (
                direction * self.acceleration * dt
            )  # Accelerate backward (opposite direction)

        # Clamp velocity to max speed
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        self.position += self.velocity * dt  # Update position based on velocity

        # Update the last movement direction
        self.last_movement = forward

    def stop(self):
        # If the player is not moving, reset velocity to zero
        if not self.is_moving:
            self.velocity = pygame.Vector2(0, 0)

    def update(self, dt, rockets=2):
        keys = pygame.key.get_pressed()

        # Player rotation controls
        if keys[pygame.K_a]:
            self.rotation_velocity = -PLAYER_TURN_SPEED  # Counter-clockwise rotation
        elif keys[pygame.K_d]:
            self.rotation_velocity = PLAYER_TURN_SPEED  # Clockwise rotation
        else:
            self.rotation_velocity = 0  # Stop rotation when no keys are pressed

        # Player movement controls
        if keys[pygame.K_w]:
            self.is_moving = True
            self.move(dt, forward=True)  # Move forward
        elif keys[pygame.K_s]:
            self.is_moving = True
            self.move(dt, forward=False)  # Move backward
        else:
            self.is_moving = False
            self.stop()  # Apply deceleration if no keys are pressed

        if keys[pygame.K_c]:
            if self.change_cooldown < 0.0:
                if self.weapon == "default":
                    self.weapon = "rocket"
                else:
                    self.weapon = "default"
                self.change_cooldown = 1

        if keys[pygame.K_SPACE]:
            if self.weapon == "rocket" and rockets > 0:
                self.shoot()
            elif self.weapon == "default":
                self.shoot()

        # Apply rotation (turning)
        self.rotate(dt)

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

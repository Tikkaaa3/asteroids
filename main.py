import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from button import Button
from constants import *
from player import Player
from shot import Shot


def main():

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    game_paused = False
    game_over = False
    score = 0
    font = pygame.font.SysFont("Arial", 24)

    background_img = pygame.image.load("images/background.png").convert()

    background_img = pygame.transform.scale(
        background_img, (SCREEN_WIDTH, SCREEN_HEIGHT)
    )

    resume_img = pygame.image.load("images/button_resume.png").convert_alpha()
    replay_img = pygame.image.load("images/button_replay.png").convert_alpha()
    quit_img = pygame.image.load("images/button_quit.png").convert_alpha()

    button_width, button_height = resume_img.get_width(), resume_img.get_height()
    quit_button_width, quit_button_height = quit_img.get_width(), quit_img.get_height()

    resume_button = Button(
        SCREEN_WIDTH / 2 - button_width / 2,
        SCREEN_HEIGHT / 2 - button_height / 2,
        resume_img,
        1,
    )

    replay_button = Button(
        SCREEN_WIDTH / 2 - button_width / 2,
        SCREEN_HEIGHT / 2 - button_height / 2,
        replay_img,
        1,
    )

    quit_button = Button(
        SCREEN_WIDTH / 2 - quit_button_width / 2,
        SCREEN_HEIGHT / 2 + button_height / 2 + 10,
        quit_img,
        1,
    )

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, drawable, updatable)
    Player.containers = (updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = [shots, updatable, drawable]

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()
    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = True
            if event.type == pygame.QUIT:
                return

        if game_paused:
            if resume_button.draw(screen):
                game_paused = False
            if quit_button.draw(screen):
                return
        elif game_over:
            if replay_button.draw(screen):
                return main()
            if quit_button.draw(screen):
                return

        else:
            screen.blit(background_img, (0, 0))
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))
            for obj in drawable:
                obj.draw(screen)

            player.cooldown -= dt
            player.change_cooldown -= dt
            updatable.update(dt)
            for obj in asteroids:
                if player.collision(obj):
                    game_over = True

            for obj in asteroids:
                for bullet in shots:
                    if bullet.collision(obj):
                        bullet.kill()
                        obj.split(player.weapon)
                        score += 100
        pygame.display.flip()

        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()

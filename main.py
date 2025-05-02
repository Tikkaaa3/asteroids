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

    creation_timer = 0.0
    lives_timer = 0.0
    game_paused = False
    game_over = False
    level_up = False
    lives = 3
    rockets = 2
    score = 0
    font = pygame.font.SysFont("Arial", 24)

    background_img = pygame.image.load("images/background.png").convert()

    background_img = pygame.transform.scale(
        background_img, (SCREEN_WIDTH, SCREEN_HEIGHT)
    )

    resume_img = pygame.image.load("images/button_resume.png").convert_alpha()
    replay_img = pygame.image.load("images/button_replay.png").convert_alpha()
    quit_img = pygame.image.load("images/button_quit.png").convert_alpha()
    lazer_img = pygame.image.load("images/lazer.png").convert_alpha()
    lazer_img = pygame.transform.scale(lazer_img, (240, 240))
    rocket_img = pygame.image.load("images/rocket.png").convert_alpha()
    rocket_img = pygame.transform.scale(rocket_img, (240, 240))

    button_width, button_height = resume_img.get_width(), resume_img.get_height()
    quit_button_width, quit_button_height = quit_img.get_width(), quit_img.get_height()
    lazer_button_width, lazer_button_height = (
        lazer_img.get_width(),
        lazer_img.get_height(),
    )

    lazer_button = Button(
        SCREEN_WIDTH / 3 - lazer_button_width / 2,
        SCREEN_HEIGHT / 3 - lazer_button_height / 2,
        lazer_img,
        1,
    )

    rocket_button = Button(
        SCREEN_WIDTH * 2 / 3 - lazer_button_width / 2,
        SCREEN_HEIGHT / 3 - lazer_button_height / 2,
        rocket_img,
        1,
    )

    resume_button = Button(
        SCREEN_WIDTH / 2 - button_width / 2,
        SCREEN_HEIGHT / 2 - button_height / 2,
        resume_img,
        1,
    )

    resume2_button = Button(
        SCREEN_WIDTH / 2 - button_width / 2,
        SCREEN_HEIGHT * 3 / 4 - button_height / 2,
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
    Player.containers = drawable
    AsteroidField.containers = updatable
    Shot.containers = [shots, updatable]

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
        if score > 1000:
            level_up = True

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
        elif level_up:
            if lazer_button.draw(screen):
                pass
            if rocket_button.draw(screen):
                if score > 100:
                    rockets += 1
                    score -= 100
            if resume2_button.draw(screen):
                score = 0
                level_up = False

        else:
            screen.blit(background_img, (0, 0))
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
            rockets_text = font.render(f"Rockets: {rockets}", True, (255, 255, 255))
            screen.blit(lives_text, (1180, 10))
            screen.blit(score_text, (10, 10))
            screen.blit(rockets_text, (580, 10))
            for obj in drawable:
                obj.draw(screen)

            for shot in shots:
                rockets = shot.draw(screen, rockets)

            player.cooldown -= dt
            player.change_cooldown -= dt
            Shot.cooldown -= dt
            updatable.update(dt)
            player.update(dt, rockets)
            for obj in asteroids:
                if player.collision(obj):
                    if lives == 0:
                        game_over = True
                    elif lives_timer < 0.0:
                        lives -= 1
                        lives_timer = 1

            if creation_timer < 0.0:
                for obj in asteroids:
                    for ast in asteroids:
                        if obj == ast:
                            continue
                        if ast.collision(obj):
                            creation_timer = 1.5
                            obj.split()
                            ast.split()

            for obj in asteroids:
                for bullet in shots:
                    if bullet.collision(obj):
                        bullet.kill()
                        obj.split(player.weapon)
                        score += 100

        creation_timer -= dt
        lives_timer -= dt
        pygame.display.flip()

        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()

import sys
import os
from time import sleep
from numpy.random import randint
import pygame

from obstacle import Obstacle
from lives import Life
from rendering import *
from sounds import *
from weapons import *

# TO DO:
# Add new weapons & ammo with varying abilities
    # rocket launch (might have to implement rate of fire for this)
# Add prices for weapons
# maybe cut levels entirely & just have speeding up of alien ships
# maybe have some alien ships that require 2+ hits to kill

R = "Right"
L = "Left"


def gameplay():
    playagain = True
    while playagain:
        intro.play(-1)
        num_levels = 5
        game_params = {
            "name": render_welcome(),
            "speed": 1,
            "weapon": Weapon1(worldx, worldy),
            "score": 0,
            "level": 0,
            "bonus_starttime": -1,
            "lives": None,
            "obstacles": None,
        }
        intro.stop()

        pygame.mixer.music.play(-1)

        levels(game_params, num_levels)
        sleep(2)
        playagain = render_final_score(
            game_params["name"], game_params["level"], game_params["score"]
        )


def levels(game_params, num_levels):
    for i in range(num_levels):
        game_params["level"] = i + 1
        game_params["bonus_starttime"] = -1
        game_params["speed"] += game_params["level"] / 2
        game_params["weapon"].mag = []
        max_score = pow(game_params["level"], 2) * 500
        initialize_lives(game_params, 3)
        initialize_obstacles(game_params, 5)

        render_level_start(
            game_params["name"], game_params["score"], game_params["level"], max_score
        )
        while game_params["score"] < max_score:
            render_backdrop(game_params["level"])
            render_score(game_params["name"], game_params["score"], max_score)
            render_lives(game_params["lives"])

            lost = roaming(game_params)
            if lost:
                return
            if pygame.time.get_ticks() > game_params["bonus_starttime"] + 5000:
                game_params["bonus_starttime"] = -1


def roaming(game_params):
    drop_obstacles(game_params)
    fire_mag(game_params)
    hit, new_bonus = check_hit(game_params)
    if new_bonus > game_params["bonus_starttime"]:
        game_params["bonus_starttime"] = new_bonus
    add_new_obstacles(game_params, hit)
    check_ammo_disappear(game_params)

    world.blit(game_params["weapon"].image, game_params["weapon"].rect)

    check_key_press(game_params)
    if check_collision(game_params) or check_misses(game_params):
        pygame.mixer.music.stop()
        crash_sound.play()
        return True

    pygame.display.flip()
    clock.tick(fps)

    return False


def check_key_press(game_params):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == ord("p"):
                pause_loop(game_params)
            if event.key == pygame.K_SPACE:
                ammo_fire.play()
                game_params["weapon"].new_ammo()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        game_params["weapon"].move(R)
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        game_params["weapon"].move(L)
    if keys[pygame.K_c]:
        game_params["weapon"].rotate(R)
    if keys[pygame.K_z]:
        game_params["weapon"].rotate(L)

    if game_params["bonus_starttime"] != -1:
        render_bonus_mode()
        if keys[pygame.K_SPACE]:
            ammo_fire.play()
            game_params["weapon"].new_ammo()


def pause_loop(game_params):
    pause_start = pygame.time.get_ticks()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == ord("q"):
                    exit_check_loop()
                    pause_stop = pygame.time.get_ticks()
                    if game_params["bonus_starttime"] != -1:
                        game_params["bonus_starttime"] += pause_stop - pause_start
                    return
                if event.key == ord("i"):
                    instructions_loop()
                    pause_stop = pygame.time.get_ticks()
                    if game_params["bonus_starttime"] != -1:
                        game_params["bonus_starttime"] += pause_stop - pause_start
                    return
                if event.key == ord("s"):
                    store_loop(game_params)
                    pause_stop = pygame.time.get_ticks()
                    if game_params["bonus_starttime"] != -1:
                        game_params["bonus_starttime"] += pause_stop - pause_start
                    return
                if event.key == ord("p"):
                    pause_stop = pygame.time.get_ticks()
                    if game_params["bonus_starttime"] != -1:
                        game_params["bonus_starttime"] += pause_stop - pause_start
                    return

        render_pause()
        pygame.display.flip()
        clock.tick(fps)


def store_loop(game_params):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    if (215 < x < 485) and (170 < y < 275):
                        if isinstance(game_params["weapon"], Weapon1):
                            continue
                        else:
                            game_params["weapon"] = Weapon1(worldx, worldy)
                            game_params["bonus_starttime"] = -1
                            return
                    if (215 < x < 485) and (300 < y < 415):
                        if isinstance(game_params["weapon"], Weapon2):
                            continue
                        else:
                            game_params["weapon"] = Weapon2(worldx, worldy)
                            game_params["bonus_starttime"] = -1
                            return
            if event.type == pygame.KEYDOWN:
                if event.key == ord("q"):
                    return

        render_store()
        pygame.display.flip()
        clock.tick(fps)


def instructions_loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return

        render_instructions()
        pygame.display.flip()
        clock.tick(fps)


def exit_check_loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == ord("y"):
                    pygame.quit()
                    sys.exit()
                if event.key == ord("n"):
                    return

        render_exit_check()
        pygame.display.flip()
        clock.tick(fps)


def initialize_lives(game_params, num):
    lives = []
    x = 50
    for i in range(num):
        new_life = Life()
        new_life.rect.midbottom = (x, new_life.rect.height + 20)
        lives.append(new_life)
        x += new_life.rect.width + 20

    game_params["lives"] = lives


def initialize_obstacles(game_params, num):
    obstacles = []
    for i in range(num):
        new_obstacle = Obstacle(game_params["level"])
        new_obstacle.rect.midbottom = (
            randint(0, worldx),
            randint(-2 * new_obstacle.rect.height, -new_obstacle.rect.height),
        )
        obstacles.append(new_obstacle)

    game_params["obstacles"] = obstacles


def add_new_obstacles(game_params, hit):
    if hit:
        new_obstacle = Obstacle(game_params["level"])
        new_obstacle.rect.midbottom = (
            randint(0, worldx),
            randint(-2 * new_obstacle.rect.height, -new_obstacle.rect.height),
        )
        game_params["obstacles"].append(new_obstacle)
    else:
        if randint(0, 50) == 8:
            new_obstacle = Obstacle(game_params["level"])
            new_obstacle.rect.midbottom = (
                randint(0, worldx),
                randint(-2 * new_obstacle.rect.height, -new_obstacle.rect.height),
            )
            game_params["obstacles"].append(new_obstacle)


def drop_obstacles(game_params):
    speed = game_params["speed"]
    for obstacle in game_params["obstacles"]:
        obstacle.drop(speed)
        world.blit(obstacle.image, obstacle.rect)


def fire_mag(game_params):
    for ammo in game_params["weapon"].mag:
        ammo.fire()
        world.blit(ammo.image, ammo.rect)


def check_misses(game_params):
    for obstacle in game_params["obstacles"]:
        if obstacle.rect.midtop[1] > worldy:
            num_lives = len(game_params["lives"])
            if num_lives == 0:
                return True
            else:
                pygame.mixer.music.pause()
                sleep(0.5)
                lost_life.play()
                sleep(0.5)
                pygame.mixer.music.unpause()
                game_params["lives"].remove(game_params["lives"][num_lives - 1])
                game_params["obstacles"].remove(obstacle)

    return False


def check_hit(game_params):
    for obstacle in game_params["obstacles"]:
        for ammo in game_params["weapon"].mag:
            if ammo.rect.colliderect(obstacle.rect):
                game_params["obstacles"].remove(obstacle)
                game_params["weapon"].remove_ammo(ammo)
                game_params["score"] += 10
                ammo_hit.play()
                if obstacle.bonus:
                    return True, pygame.time.get_ticks()
                return True, -1

    return False, -1


def check_collision(game_params):
    for obstacle in game_params["obstacles"]:
        if game_params["weapon"].rect.colliderect(obstacle.rect):
            game_params["weapon"].collisions -= 1
            game_params["obstacles"].remove(obstacle)
            crash_sound.play()
            if game_params["weapon"].collisions == 0:
                return True

    return False


def check_ammo_disappear(game_params):
    for ammo in game_params["weapon"].mag:
        if (ammo.rect.midbottom[0] < 0 or ammo.rect.midbottom[0] > worldx) and (
            ammo.rect.midbottom[1] < 0 or ammo.rect.midbottom[1] > worldy
        ):
            game_params["weapon"].remove_ammo(ammo)


if __name__ == "__main__":
    pygame.init()
    gameplay()
    pygame.quit()

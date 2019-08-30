import pygame
import sys

from numpy.random import randint
from time import sleep

pygame.font.init()
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

fps = 40
worldx = 1000
worldy = 600

world = pygame.display.set_mode([worldx, worldy])
backdropbox = world.get_rect()

font_extra_small = pygame.font.Font("freesansbold.ttf", 10)
font_small = pygame.font.Font("freesansbold.ttf", 20)
font_med = pygame.font.Font("freesansbold.ttf", 40)
font_large = pygame.font.Font("freesansbold.ttf", 60)


def render_level_start(name, score, level, max_score):
    starttime = pygame.time.get_ticks()
    scorecard = font_small.render(f"{name}'s Score :: {score}/{max_score}", True, WHITE)
    scorecard_rect = scorecard.get_rect()
    scorecard_rect.topright = (worldx - 30, 30)

    welcome_vis = font_med.render("Now beginning...", True, WHITE)
    welcome_rect = welcome_vis.get_rect()
    welcome_rect.center = (worldx / 2, worldy / 3 - 75)

    level_vis = font_large.render(f"Level {level}", True, WHITE)
    level_rect = level_vis.get_rect()
    level_rect.center = (worldx / 2, worldy / 3)

    while True:
        pre_world = pygame.display.set_mode([worldx, worldy])
        pre_world.fill(BLACK)
        pre_world.blit(scorecard, scorecard_rect)
        pre_world.blit(welcome_vis, welcome_rect)
        pre_world.blit(level_vis, level_rect)
        pygame.display.flip()
        clock.tick(fps)
        if pygame.time.get_ticks() > starttime + 5000:
            break


def render_backdrop(level):
    backdrop = pygame.image.load(f"images/level{level}.png").convert()
    world.blit(backdrop, backdropbox)


def render_exit_check():
    color = (randint(0, 255), randint(0, 255), randint(0, 255))
    check = font_small.render(
        "Are you sure you want to exit? (y/n)", True, color, BLACK
    )
    check_rect = check.get_rect()
    check_rect.center = (worldx / 2, worldy / 2)
    world.blit(check, check_rect)


def render_score(name, score, max_score):
    scorecard = font_small.render(f"{name}'s Score :: {score}/{max_score}", True, WHITE)
    scorecard_rect = scorecard.get_rect()
    scorecard_rect.topright = (worldx - 30, 30)
    world.blit(scorecard, scorecard_rect)


def render_bonus_mode():
    color = (randint(0, 255), randint(0, 255), randint(0, 255))
    bonus_mode = font_small.render("B O N U S  M O D E", True, color, BLACK)
    bonus_rect = bonus_mode.get_rect()
    bonus_rect.midtop = (worldx / 2, 30)
    world.blit(bonus_mode, bonus_rect)


def render_pause():
    color = (randint(0, 255), randint(0, 255), randint(0, 255))
    pause = font_small.render("P A U S E D", True, color, BLACK)
    pause_rect = pause.get_rect()
    pause_rect.center = (worldx / 2, worldy / 2)

    instruc = font_extra_small.render("Press 'i' for instructions", True, WHITE, BLACK)
    instruc_rect = instruc.get_rect()
    instruc_rect.center = (worldx / 2, worldy / 2 + 30)

    world.blit(instruc, instruc_rect)
    world.blit(pause, pause_rect)


def render_instructions():
    instruc = pygame.image.load(f"images/instructions.png").convert()
    instruc_rect = instruc.get_rect()
    instruc_rect.center = (worldx / 2, worldy / 2)

    color = (randint(0, 255), randint(0, 255), randint(0, 255))
    world.blit(instruc, instruc_rect)
    pygame.draw.rect(world, color, instruc_rect, 2)


def render_welcome():
    header_vis = font_med.render("Welcome to", True, WHITE)
    header_rect = header_vis.get_rect()
    header_rect.center = (worldx / 2, worldy / 4)

    credit_vis = font_extra_small.render("A Game By Jordan Lueck", True, WHITE)
    credit_rect = credit_vis.get_rect()
    credit_rect.center = (worldx / 2, worldy / 3 + 80)

    type_name = font_small.render("Type your name, then press enter...", True, WHITE)
    type_name_rect = type_name.get_rect()
    type_name_rect.center = (worldx / 2, worldy / 2 + 50)

    name = []
    while True:
        color = (randint(0, 255), randint(0, 255), randint(0, 255))
        game_vis = font_large.render("S P A C E  F O R C E", True, color)
        game_rect = game_vis.get_rect()
        game_rect.center = (worldx / 2, worldy / 3 + 20)

        name_vis = font_large.render("".join(name), True, WHITE)
        name_rect = name_vis.get_rect()
        name_rect.center = (worldx / 2, worldy - 150)

        welcome_world = pygame.display.set_mode([worldx, worldy])
        welcome_world.fill(BLACK)
        welcome_world.blit(header_vis, header_rect)
        welcome_world.blit(game_vis, game_rect)
        welcome_world.blit(credit_vis, credit_rect)
        welcome_world.blit(type_name, type_name_rect)
        welcome_world.blit(name_vis, name_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if (event.key == 32) or (97 <= event.key <= 122):
                    letter = chr(event.key)
                    if pygame.key.get_mods() & pygame.KMOD_CAPS:
                        letter = letter.upper()
                    name.append(letter)
                if event.key == 8 and len(name) > 0:
                    name.remove(name[len(name) - 1])
                if event.key == 13:
                    sleep(1)
                    return "".join(name)

        pygame.display.flip()
        clock.tick(fps)


def render_final_score(name, level, score):

    level_vis = font_med.render(f"You made it to Level {level}", True, WHITE)
    level_rect = level_vis.get_rect()
    level_rect.center = (worldx / 2, worldy / 3 + 20)

    score_vis = font_small.render(f"Your Final Score was {score}", True, WHITE)
    score_rect = score_vis.get_rect()
    score_rect.center = (worldx / 2, worldy / 2 - 30)

    hs_header = font_small.render("High Scores", True, (54, 159, 250))
    hs_header_rect = hs_header.get_rect()
    hs_header_rect.center = (worldx / 2, worldy / 2 + 40)

    info_vis = font_extra_small.render(
        "Press 'q' to exit, and 'r' to play again!", True, WHITE
    )
    info_rect = info_vis.get_rect()
    info_rect.center = (worldx - info_rect.width, worldy - 50)

    with open("scores/highscores.txt", "r") as hs:
        scores = hs.readlines()

    inserted = False
    for i in range(len(scores)):
        this_score = int(scores[i].strip("\n").split(",")[1])
        if not inserted and score > this_score:
            scores.insert(i, f"{name},{score}\n")
            inserted = True
            break
    if not inserted:
        scores.append(f"{name},{score}\n")

    with open("scores/highscores.txt", "w") as hs:
        hs.writelines(scores)

    while True:
        color = (randint(0, 255), randint(0, 255), randint(0, 255))
        header_vis = font_large.render(f"Congratulations {name}!", True, color)
        header_rect = header_vis.get_rect()
        header_rect.center = (worldx / 2, worldy / 4)

        post_world = pygame.display.set_mode([worldx, worldy])
        post_world.fill(BLACK)
        post_world.blit(header_vis, header_rect)
        post_world.blit(level_vis, level_rect)
        post_world.blit(score_vis, score_rect)
        post_world.blit(hs_header, hs_header_rect)
        post_world.blit(info_vis, info_rect)

        yloc = worldy / 2 + 70
        for i in range(5):
            player_data = scores[i].strip("\n").split(",")

            hs_name_vis = font_extra_small.render(f"{player_data[0]}", True, WHITE)
            hs_name_rect = hs_name_vis.get_rect()
            hs_name_rect.topleft = (worldx / 2 - 70, yloc)

            hs_score_vis = font_extra_small.render(f"{player_data[1]}", True, WHITE)
            hs_score_rect = hs_score_vis.get_rect()
            hs_score_rect.topright = (worldx / 2 + 70, yloc)

            post_world.blit(hs_name_vis, hs_name_rect)
            post_world.blit(hs_score_vis, hs_score_rect)
            yloc += 20
            if i == len(scores) - 1:
                break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == ord("q"):
                    pygame.quit()
                    sys.exit()
                if event.key == ord("r"):
                    return True

        pygame.display.flip()
        clock.tick(fps)

    return False


def render_lives(lives):
    for life in lives:
        world.blit(life.image, life.rect)

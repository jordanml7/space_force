import sys
import os
from time import sleep
from numpy.random import randint
import pygame

from player import Player
from obstacle import Obstacle
from lives import Life

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def gameplay():
    game = SpaceForce(1000, 600, 40, 15, 1)
    name = run_welcome()
    playagain = True
    while playagain:
        player = Player(worldx, worldy)
        score, level = levels(name, player)
        playagain = run_final_score(name, level, score)


class SpaceForce:
    def __init__(self, worldx, worldy, fps, steps, init_speed):
        self.clock = pygame.time.Clock()
        pygame.init()

        self.set_sounds()
        self.set_fonts()

        self.worldx = worldx
        self.worldy = worldy
        self.fps = fps
        self.steps = steps
        self.speed = init_speed
        self.score = 0
        self.max_score = -1
        self.level = -1

        self.world = pygame.display.set_mode([self.worldx, self.worldy])
        self.backdropbox = self.world.get_rect()

        self.name = self.run_welcome()

        self.player = Player(self.worldx, self.worldy)

    def set_sounds(self):
        pygame.mixer.music.load("music/Relapse.wav")
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(-1)

        self.laser_hit = pygame.mixer.Sound("music/explosion.wav")
        self.laser_hit.set_volume(0.3)

        self.crash_sound = pygame.mixer.Sound("music/boom.wav")
        self.crash_sound.set_volume(0.3)

        self.lost_life = pygame.mixer.Sound("music/alarm.wav")
        self.lost_life.set_volume(1)

        self.laser_fire = pygame.mixer.Sound("music/laser.wav")
        self.laser_fire.set_volume(0.5)

    def set_fonts(self):
        self.font_extra_small = pygame.font.Font("freesansbold.ttf", 10)
        self.font_small = pygame.font.Font("freesansbold.ttf", 20)
        self.font_med = pygame.font.Font("freesansbold.ttf", 40)
        self.font_large = pygame.font.Font("freesansbold.ttf", 60)

    def run_welcome(self):
        header_vis = self.font_med.render("Welcome to", True, WHITE)
        header_rect = header_vis.get_rect()
        header_rect.center = (self.worldx / 2, self.worldy / 4)

        credit_vis = self.font_extra_small.render("A Game By Jordan Lueck", True, WHITE)
        credit_rect = credit_vis.get_rect()
        credit_rect.center = (self.worldx / 2, self.worldy / 3 + 80)

        instruc_vis = self.font_small.render(
            "Type your name, then press enter...", True, WHITE
        )
        instruc_rect = instruc_vis.get_rect()
        instruc_rect.center = (self.worldx / 2, self.worldy / 2 + 50)

        name = []
        while True:
            game_vis = self.font_large.render(
                "S P A C E  F O R C E",
                True,
                (randint(0, 255), randint(0, 255), randint(0, 255)),
            )
            game_rect = game_vis.get_rect()
            game_rect.center = (self.worldx / 2, self.worldy / 3 + 20)

            name_vis = self.font_large.render("".join(name), True, WHITE)
            name_rect = name_vis.get_rect()
            name_rect.center = (self.worldx / 2, self.worldy - 150)

            # welcome_world = pygame.display.set_mode([worldx, worldy])
            self.world.fill(BLACK)
            self.world.blit(header_vis, header_rect)
            self.world.blit(game_vis, game_rect)
            self.world.blit(credit_vis, credit_rect)
            self.world.blit(instruc_vis, instruc_rect)
            self.world.blit(name_vis, name_rect)

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
            self.clock.tick(self.fps)

        def levels(self):
            for i in range(5):
                self.level = i + 1
                self.max_score = pow(self.level, 2) * 500
                self.speed += self.level / 2
                self.lives = initialize_lives(3)
                self.obstacles = initialize_obstacles(5, level)
                self.player.lasers = []
                level_start(pygame.time.get_ticks(), level, name, score, max_score)
                while score < max_score:
                    exit, score = roaming(
                        name, player, obstacles, speed, level, lives, score, max_score
                    )
                    if exit:
                        sleep(2)
                        return score, level

            return score, level


def run_final_score(name, level, score):
    header_vis = font_large.render(f"Congratulations {name}!", True, (160, 218, 43))
    header_rect = header_vis.get_rect()
    header_rect.center = (worldx / 2, worldy / 3)

    level_vis = font_med.render(f"You made it to Level {level}", True, WHITE)
    level_rect = level_vis.get_rect()
    level_rect.center = (worldx / 2, worldy / 2)

    score_vis = font_small.render(f"Your Final Score was {score}", True, WHITE)
    score_rect = score_vis.get_rect()
    score_rect.center = (worldx / 2, worldy / 2 + 50)

    info_vis = font_extra_small.render(
        "Press 'q' to exit, and 'r' to play again!", True, WHITE
    )
    info_rect = info_vis.get_rect()
    info_rect.center = (worldx / 2, worldy - 50)

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
        post_world = pygame.display.set_mode([worldx, worldy])
        post_world.fill(BLACK)
        post_world.blit(header_vis, header_rect)
        post_world.blit(level_vis, level_rect)
        post_world.blit(score_vis, score_rect)
        post_world.blit(info_vis, info_rect)

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


def level_start(starttime, level, name, score, max_score):
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


def roaming(name, player, obstacles, speed, level, lives, score, max_score):
    backdrop = pygame.image.load(f"images/level{level}.png").convert()
    world.blit(backdrop, backdropbox)
    render_score(name, score, max_score)
    render_lives(lives)

    player.orient()
    player.update()
    world.blit(player.image, player.rect)

    drop_obstacles(obstacles, speed)
    fire_lasers(player)
    hit = False
    if check_hit(player, obstacles):
        hit = True
        laser_hit.play()
        score += 10
    add_new_obstacles(obstacles, level, hit)
    check_laser_disappear(player)

    check_key_press(player)
    if check_collision(player, obstacles) or check_misses(obstacles, lives):
        pygame.mixer.music.stop()
        crash_sound.play()
        return True, score

    pygame.display.flip()
    clock.tick(fps)

    return False, score


def render_lives(lives):
    for life in lives:
        world.blit(life.image, life.rect)


def render_score(name, score, max_score):
    scorecard = font_small.render(f"{name}'s Score :: {score}/{max_score}", True, WHITE)
    scorecard_rect = scorecard.get_rect()
    scorecard_rect.topright = (worldx - 30, 30)
    world.blit(scorecard, scorecard_rect)


def check_key_press(player):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == ord("q"):
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_RIGHT or event.key == ord("d"):
                player.orientation = "Right"
                player.control(steps, 0)
            if event.key == pygame.K_LEFT or event.key == ord("a"):
                player.orientation = "Left"
                player.control(-steps, 0)
            if event.key == pygame.K_SPACE:
                laser_fire.play()
                player.new_laser()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == ord("d"):
                player.control(-steps, 0)
            if event.key == pygame.K_LEFT or event.key == ord("a"):
                player.control(steps, 0)


def initialize_lives(num):
    lives = []
    x = 30
    for i in range(num):
        new_life = Life()
        new_life.rect.midbottom = (x, new_life.rect.height + 20)
        lives.append(new_life)
        x += new_life.rect.width + 30

    return lives


def initialize_obstacles(num, level):
    obstacles = []
    for i in range(num):
        new_obstacle = Obstacle(level)
        new_obstacle.rect.midbottom = (
            randint(0, worldx),
            randint(-2 * new_obstacle.rect.height, -new_obstacle.rect.height),
        )
        obstacles.append(new_obstacle)

    return obstacles


def add_new_obstacles(obstacles, level, hit):
    if hit:
        new_obstacle = Obstacle(level)
        new_obstacle.rect.midbottom = (
            randint(0, worldx),
            randint(-2 * new_obstacle.rect.height, -new_obstacle.rect.height),
        )
        obstacles.append(new_obstacle)
    else:
        if randint(0, 50) == 8:
            new_obstacle = Obstacle(level)
            new_obstacle.rect.midbottom = (
                randint(0, worldx),
                randint(-2 * new_obstacle.rect.height, -new_obstacle.rect.height),
            )
            obstacles.append(new_obstacle)


def drop_obstacles(obstacles, speed):
    for obstacle in obstacles:
        obstacle.drop(speed)
        world.blit(obstacle.image, obstacle.rect)


def fire_lasers(player):
    for laser in player.lasers:
        laser.fire()
        world.blit(laser.image, laser.rect)


def check_misses(obstacles, lives):
    for obstacle in obstacles:
        if obstacle.rect.midtop[1] > worldy:
            if len(lives) == 0:
                return True
            else:
                pygame.mixer.music.pause()
                lost_life.play()
                pygame.mixer.music.unpause()
                lives.remove(lives[len(lives) - 1])
                obstacles.remove(obstacle)

    return False


def check_hit(player, obstacles):
    for obstacle in obstacles:
        for laser in player.lasers:
            if laser.rect.colliderect(obstacle.rect):
                if obstacle.bonus:
                    rapid_fire
                obstacles.remove(obstacle)
                player.remove_laser(laser)
                return True

    return False


def check_collision(player, obstacles):
    for obstacle in obstacles:
        if player.rect.colliderect(obstacle.rect):
            return True

    return False


def check_laser_disappear(player):
    for laser in player.lasers:
        if (laser.rect.midbottom[0] < 0 or laser.rect.midbottom[0] > worldx) and (
            laser.rect.midbottom[1] < 0 or laser.rect.midbottom[1] > worldy
        ):
            player.remove_laser(laser)


if __name__ == "__main__":
    gameplay()

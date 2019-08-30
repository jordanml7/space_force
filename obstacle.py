import pygame
from numpy.random import randint


class Obstacle(pygame.sprite.Sprite):
    """
    Spawn an obstacle
    """

    def __init__(self, level):
        pygame.sprite.Sprite.__init__(self)

        self.bonus = False
        if randint(1, 70) == 8:
            self.bonus = True

        if self.bonus:
            bonus = pygame.image.load(f"images/bonus_obstacle.png").convert()
            bonus.convert_alpha()
            ALPHA = bonus.get_at((1, 1))
            bonus.set_colorkey(ALPHA)  # set alpha
            self.image = bonus
        else:
            image = pygame.image.load(f"images/level{level}_obstacle.png").convert()
            image.convert_alpha()  # optimise alpha
            ALPHA = image.get_at((1, 1))
            image.set_colorkey(ALPHA)  # set alpha
            self.image = image

        self.rect = self.image.get_rect()

    def drop(self, speed):
        self.rect.move_ip(0, speed)

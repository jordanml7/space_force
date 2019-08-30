import pygame
from math import sin, cos, radians


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        pygame.sprite.Sprite.__init__(self)

        self.angle = angle
        laser = pygame.image.load("images/laser.png").convert()
        laser_rot = pygame.transform.rotozoom(laser, self.angle, 1)
        laser_rot.convert_alpha()  # optimise alpha
        ALPHA = laser_rot.get_at((0, 0))
        laser_rot.set_colorkey(ALPHA)  # set alpha
        self.image = laser_rot

        """
        self.orientation = orientation
        if self.orientation == "Right":
            self.image = pygame.transform.flip(self.orig_image, True, False)
        elif self.orientation == "Left":
            self.image = self.orig_image
        """

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def fire(self, rate):
        self.rect.x -= rate * sin(radians(self.angle))
        self.rect.y -= rate * cos(radians(self.angle))
        """
        if self.orientation == "Right":
            self.rect.x += rate
            self.rect.y -= rate
        elif self.orientation == "Left":
            self.rect.x -= rate
            self.rect.y -= rate
        """

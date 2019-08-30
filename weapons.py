import pygame
from math import sin, cos, radians
from ammo import Laser


class Weapon(pygame.sprite.Sprite):
    """
    Spawn a player
    """

    def __init__(self, worldx, worldy, num):
        pygame.sprite.Sprite.__init__(self)

        self.worldx = worldx
        self.worldy = worldy
        self.weapon = num

        img = pygame.image.load(f"images/player{self.weapon}.png").convert()
        img.convert_alpha()  # optimise alpha
        ALPHA = img.get_at((0, 0))
        img.set_colorkey(ALPHA)  # set alpha
        self.orig_image = img

        self.image = self.orig_image
        self.rect = self.image.get_rect()
        self.rect.center = ((self.worldx / 2), self.worldy - 25)

        self.lasers = []

        self.orientation = "Left"
        self.movex = 0  # move along X

        self.angle = 0

    def control(self, x):
        """
        control player movement
        """
        self.movex += x

    def reset_moving(self):
        self.movex = 0

    def update(self):
        """
        Update sprite position
        """
        self.rect.x += self.movex

        if self.rect.x >= self.worldx - self.rect.width:
            self.rect.x = self.worldx - self.rect.width
        elif self.rect.x <= 0:
            self.rect.x = 0

    def rotate(self):
        if self.angle > 50:
            self.angle = 50
        elif self.angle < -50:
            self.angle = -50

        pivot = self.rect.center
        img = pygame.transform.rotozoom(self.orig_image, self.angle, 1)
        img.convert_alpha()  # optimise alpha
        ALPHA = img.get_at((0, 0))
        img.set_colorkey(ALPHA)  # set alpha

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = pivot

    def orient(self):
        if self.orientation == "Right":
            self.image = pygame.transform.flip(self.orig_image, True, False)
        elif self.orientation == "Left":
            self.image = self.orig_image

    def new_laser(self):
        new_laser = Laser(self.rect.center[0], self.rect.center[1], self.angle)
        """
        if self.orientation == "Right":
            new_laser = Laser(
                self.rect.topright[0], self.rect.topright[1], self.orientation
            )
        else:
            new_laser = Laser(
                self.rect.topleft[0], self.rect.topleft[1], self.orientation
            )
        """
        self.lasers.append(new_laser)

    def remove_laser(self, laser):
        self.lasers.remove(laser)
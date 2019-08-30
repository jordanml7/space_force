import pygame
from math import sin, cos, radians
from ammo import *


class Weapon1(pygame.sprite.Sprite):
    """
    Spawn a player
    """

    def __init__(self, worldx, worldy):
        pygame.sprite.Sprite.__init__(self)

        self.worldx = worldx
        self.worldy = worldy

        img = pygame.image.load(f"images/weapons/weapon1.png").convert()
        img.convert_alpha()  # optimise alpha
        ALPHA = img.get_at((0, 0))
        img.set_colorkey(ALPHA)  # set alpha
        self.orig_image = img

        self.image = self.orig_image
        self.rect = self.image.get_rect()
        self.rect.midbottom = ((self.worldx / 2), self.worldy)

        self.mag = []
        self.orientation = "Right"
        self.speed = 15
        self.collisions = 1

    def move(self, dir):
        """
        Update sprite position
        """
        if dir == "Right":
            self.orientation = "Right"
            self.rect.x += self.speed
        else:
            self.orientation = "Left"
            self.rect.x -= self.speed
        self.orient()

        if self.rect.x >= self.worldx - self.rect.width:
            self.rect.x = self.worldx - self.rect.width
        elif self.rect.x <= 0:
            self.rect.x = 0

    def orient(self):
        if self.orientation == "Right":
            self.image = pygame.transform.flip(self.orig_image, True, False)
        elif self.orientation == "Left":
            self.image = self.orig_image

    def rotate(self):
        pass  # does nothing for Weapon 1

    def new_ammo(self):
        if self.orientation == "Right":
            new_laser = BlueLaser(
                self.rect.topright[0], self.rect.topright[1], self.orientation
            )
        else:
            new_laser = BlueLaser(
                self.rect.topleft[0], self.rect.topleft[1], self.orientation
            )
        self.mag.append(new_laser)

    def remove_ammo(self, laser):
        self.mag.remove(laser)


class Weapon2(pygame.sprite.Sprite):
    """
    Spawn a player
    """

    def __init__(self, worldx, worldy):
        pygame.sprite.Sprite.__init__(self)

        self.worldx = worldx
        self.worldy = worldy

        img = pygame.image.load(f"images/weapons/weapon2.png").convert()
        img.convert_alpha()  # optimise alpha
        ALPHA = img.get_at((0, 0))
        img.set_colorkey(ALPHA)  # set alpha
        self.orig_image = img

        self.image = self.orig_image
        self.rect = self.image.get_rect()
        self.rect.center = ((self.worldx / 2), self.worldy - 25)

        self.mag = []
        self.angle = 0
        self.speed = 12
        self.angular_speed = 5
        self.collisions = 2

    def move(self, dir):
        """
        Update sprite position
        """
        if dir == "Right":
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

        if self.rect.x >= self.worldx - self.rect.width:
            self.rect.x = self.worldx - self.rect.width
        elif self.rect.x <= 0:
            self.rect.x = 0

    def rotate(self, dir):
        if dir == "Right":
            self.angle -= self.angular_speed
        else:
            self.angle += self.angular_speed

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

    def new_ammo(self):
        new_laser = RedLaser(self.rect.center[0], self.rect.center[1], self.angle)
        self.mag.append(new_laser)

    def remove_ammo(self, laser):
        self.mag.remove(laser)

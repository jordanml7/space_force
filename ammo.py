import pygame
from math import sin, cos, radians


class BlueLaser(pygame.sprite.Sprite):
    def __init__(self, x, y, orientation):
        pygame.sprite.Sprite.__init__(self)

        laser = pygame.image.load("images/ammo/blue_laser.png").convert()
        laser = pygame.transform.rotate(laser, 45)
        laser.convert_alpha()  # optimise alpha
        ALPHA = laser.get_at((0, 0))
        laser.set_colorkey(ALPHA)  # set alpha
        self.orig_image = laser

        self.orientation = orientation
        if self.orientation == "Right":
            self.image = pygame.transform.flip(self.orig_image, True, False)
        elif self.orientation == "Left":
            self.image = self.orig_image

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.update_damage_rect()

        self.rate = 5

    def fire(self):
        if self.orientation == "Right":
            self.rect.x += self.rate
            self.rect.y -= self.rate
        elif self.orientation == "Left":
            self.rect.x -= self.rate
            self.rect.y -= self.rate
        self.update_damage_rect()

    def update_damage_rect(self):
        self.damage_rect = self.rect.copy()


class RedLaser(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        pygame.sprite.Sprite.__init__(self)

        self.angle = 90-angle
        laser = pygame.image.load("images/ammo/red_laser.png").convert()
        laser_rot = pygame.transform.rotozoom(laser, self.angle, 1)
        laser_rot.convert_alpha()  # optimise alpha
        ALPHA = laser_rot.get_at((0, 0))
        laser_rot.set_colorkey(ALPHA)  # set alpha
        self.image = laser_rot

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.update_damage_rect()

        self.rate = 4

    def fire(self):
        self.rect.x -= self.rate * sin(radians(self.angle))
        self.rect.y -= self.rate * cos(radians(self.angle))
        self.update_damage_rect()

    def update_damage_rect(self):
        self.damage_rect = self.rect.copy()


class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y, orientation):
        pygame.sprite.Sprite.__init__(self)

        laser = pygame.image.load("images/ammo/missile.png").convert()
        laser = pygame.transform.rotate(laser, 45)
        laser.convert_alpha()  # optimise alpha
        ALPHA = laser.get_at((0, 0))
        laser.set_colorkey(ALPHA)  # set alpha
        self.orig_image = laser

        self.orientation = orientation
        if self.orientation == "Right":
            self.image = pygame.transform.flip(self.orig_image, True, False)
        elif self.orientation == "Left":
            self.image = self.orig_image

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.update_damage_rect()

        self.rate = 2

    def fire(self):
        if self.orientation == "Right":
            self.rect.x += self.rate
            self.rect.y -= self.rate
        elif self.orientation == "Left":
            self.rect.x -= self.rate
            self.rect.y -= self.rate
        self.update_damage_rect()

    def update_damage_rect(self):
        self.damage_rect = self.rect.inflate(200, 200)

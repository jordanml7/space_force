import pygame
from math import sin, cos, radians
from ammo import *
from sounds import *

weapons_info = [
    {
        "speed": 15,
        "movement": "Strafing",
        "angles": "-45 & 45 deg",
        "strength": "Level 1",
        "rof": 5,
        "ammo": "Blue Laser",
        "ammo_strength": "Average",
        "ammo_speed": 5,
        "cost": 100,
    },
    {
        "speed": 12,
        "movement": "Strafing & Rotation",
        "angles": "-50 to 50 deg",
        "strength": "Level 2",
        "rof": 3,
        "ammo": "Red Laser",
        "ammo_strength": "Average",
        "ammo_speed": 4,
        "cost": 200,
    },
    {
        "speed": 5,
        "movement": "Strafing",
        "angles": "-45 & 45 deg",
        "strength": "Level 3",
        "rof": 1,
        "ammo": "Missile",
        "ammo_strength": "High",
        "ammo_speed": 1,
        "cost": 300,
    },
]


class Weapon1(pygame.sprite.Sprite):
    """
    Spawn a player
    """

    def __init__(self, worldx, worldy):
        pygame.sprite.Sprite.__init__(self)

        self.worldx = worldx
        self.worldy = worldy

        img = pygame.image.load(f"images/weapons/weapon1.png").convert_alpha()
        self.orig_image = img

        self.image = self.orig_image
        self.rect = self.image.get_rect()
        self.rect.midbottom = ((self.worldx / 2), self.worldy)

        self.mag = []
        self.orientation = "Left"
        self.speed = 15
        self.collisions = 1

        self.rof = 5  # shots per second
        self.curr_rof = self.rof
        self.last_fire = -1

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

    def rotate(self, dir):
        pass  # does nothing for Weapon 1

    def new_ammo(self, time):
        if time < self.last_fire + 1000 / self.curr_rof:
            return

        ammo_fire.play()
        if self.orientation == "Right":
            new_laser = BlueLaser(
                self.rect.topright[0], self.rect.topright[1], self.orientation
            )
        else:
            new_laser = BlueLaser(
                self.rect.topleft[0], self.rect.topleft[1], self.orientation
            )
        self.last_fire = time
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

        img = pygame.image.load(f"images/weapons/weapon2/90.png").convert_alpha()
        self.orig_image = img

        self.image = self.orig_image
        self.rect = self.image.get_rect()
        self.rect.midbottom = ((self.worldx / 2), self.worldy)

        self.mag = []
        self.angle = 90
        self.speed = 12
        self.angular_speed = 10
        self.collisions = 2

        self.rof = 3  # shots per second
        self.curr_rof = self.rof
        self.last_fire = -1

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
        orig_center = self.rect.midbottom
        if dir == "Right":
            self.angle += self.angular_speed
        else:
            self.angle -= self.angular_speed

        if self.angle < 20:
            self.angle = 20
        elif self.angle > 160:
            self.angle = 160

        if self.angle > 90:
            img = pygame.image.load(f"images/weapons/weapon2/{180 - self.angle}.png").convert_alpha()
            img = pygame.transform.flip(img, True, False)
        else:
            img = pygame.image.load(f"images/weapons/weapon2/{self.angle}.png").convert_alpha()
        
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midbottom = orig_center

    def new_ammo(self, time):
        if time < self.last_fire + 1000 / self.curr_rof:
            return

        ammo_fire.play()
        new_laser = RedLaser(self.rect.midbottom[0], self.rect.midbottom[1] - 20, self.angle)
        self.last_fire = time
        self.mag.append(new_laser)

    def remove_ammo(self, laser):
        self.mag.remove(laser)


class Weapon3(pygame.sprite.Sprite):
    """
    Spawn a player
    """

    def __init__(self, worldx, worldy):
        pygame.sprite.Sprite.__init__(self)

        self.worldx = worldx
        self.worldy = worldy

        img = pygame.image.load(f"images/weapons/weapon3.png").convert()
        img.convert_alpha()  # optimise alpha
        ALPHA = img.get_at((0, 0))
        img.set_colorkey(ALPHA)  # set alpha
        self.orig_image = img

        self.image = self.orig_image
        self.rect = self.image.get_rect()
        self.rect.midbottom = ((self.worldx / 2), self.worldy)

        self.mag = []
        self.orientation = "Left"
        self.speed = 5
        self.collisions = 3

        self.rof = 1  # launches per second
        self.curr_rof = self.rof
        self.last_fire = -1

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

    def rotate(self, dir):
        pass  # does nothing for Weapon 3

    def new_ammo(self, time):
        if time < self.last_fire + 1000 / self.curr_rof:
            return

        ammo_fire.play()
        if self.orientation == "Right":
            new_missile = Missile(
                self.rect.topright[0], self.rect.topright[1], self.orientation
            )
        else:
            new_missile = Missile(
                self.rect.topleft[0], self.rect.topleft[1], self.orientation
            )
        self.last_fire = time
        self.mag.append(new_missile)

    def remove_ammo(self, missile):
        self.mag.remove(missile)

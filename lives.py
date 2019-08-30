import pygame


class Life(pygame.sprite.Sprite):
    """
    Spawn an obstacle
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        img = pygame.image.load("images/life.png").convert()
        img.convert_alpha()  # optimise alpha
        ALPHA = img.get_at((1, 1))
        img.set_colorkey(ALPHA)  # set alpha

        self.image = img
        self.rect = self.image.get_rect()

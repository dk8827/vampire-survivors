import pygame

class Gem(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("gem.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (25, 20))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

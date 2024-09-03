import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy, speed=10):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
        self.dx = dx
        self.dy = dy

    def update(self):
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed
        if not pygame.display.get_surface().get_rect().contains(self.rect):
            self.kill()

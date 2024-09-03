import pygame
import random
import math

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.rect.x = random.randint(0, screen.get_width() - self.rect.width)
        self.rect.y = random.choice([0, screen.get_height() - self.rect.height])
        self.speed = random.uniform(0.5, 2)
        self.hp = 10  # Add hp attribute

    def update(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx, dy = dx / dist, dy / dist
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.kill()
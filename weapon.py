import math
import random
import pygame
from projectile import Projectile

class Weapon:
    def __init__(self, name, level):
        self.name = name
        self.level = level

    def level_up(self):
        self.level += 1

    def attack(self, x, y, projectiles):
        pass

class Knife(Weapon):
    def attack(self, x, y, projectiles):
        for angle in range(0, 360, 360 // (self.level + 1)):
            rad = math.radians(angle)
            dx = math.cos(rad)
            dy = math.sin(rad)
            projectiles.add(Projectile(x, y, dx, dy))

class Axe(Weapon):
    def attack(self, x, y, projectiles):
        for _ in range(self.level):
            angle = math.radians(random.randint(0, 360))
            dx = math.cos(angle)
            dy = math.sin(angle)
            projectiles.add(Projectile(x, y, dx, dy, speed=5))

class Fireball(Weapon):
    def attack(self, x, y, projectiles):
        for _ in range(self.level):
            angle = math.radians(random.randint(0, 360))
            dx = math.cos(angle)
            dy = math.sin(angle)
            projectiles.add(Projectile(x, y, dx, dy, speed=7))

class Garlic(Weapon):
    def __init__(self, name, level):
        super().__init__(name, level)
        self.radius = 100
        self.damage = 1

    def level_up(self):
        super().level_up()
        self.radius += 10
        self.damage += 0.5

    def attack(self, x, y, projectiles):
        # Garlic doesn't create projectiles, it damages enemies within its radius
        pass

    def draw(self, screen, x, y):
        pygame.draw.circle(screen, (200, 200, 200), (x, y), self.radius, 2)
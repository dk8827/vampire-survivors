import math
import random
import pygame
from projectile import Projectile

class Weapon:
    def __init__(self, name, level):
        self.name = name
        self.level = level
        self.cooldown = 30  # Default cooldown, can be overridden in subclasses
        self.current_cooldown = 0

    def level_up(self):
        self.level += 1

    def attack(self, x, y, projectiles):
        if self.current_cooldown <= 0:
            self._perform_attack(x, y, projectiles)
            self.current_cooldown = self.cooldown
        else:
            self.current_cooldown -= 1

    def _perform_attack(self, x, y, projectiles):
        pass  # To be implemented by subclasses

class Knife(Weapon):
    def __init__(self, name, level):
        super().__init__(name, level)
        self.cooldown = 15  # Faster cooldown for knife

    def _perform_attack(self, x, y, projectiles):
        for angle in range(-30, 31, 60):  # Shoot 3 knives in a spread
            rad = math.radians(angle)
            dx = math.cos(rad)
            dy = math.sin(rad)
            projectiles.add(Projectile(x, y, dx, dy))

class Axe(Weapon):
    def _perform_attack(self, x, y, projectiles):
        for _ in range(self.level):
            angle = math.radians(random.randint(0, 360))
            dx = math.cos(angle)
            dy = math.sin(angle)
            projectiles.add(Projectile(x, y, dx, dy, speed=5))

class Fireball(Weapon):
    def _perform_attack(self, x, y, projectiles):
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
        self.cooldown = max(15, self.cooldown - 2)

    def attack(self, x, y, projectiles, enemies):
        if self.current_cooldown <= 0:
            for enemy in enemies:
                if pygame.math.Vector2(x, y).distance_to(enemy.rect.center) <= self.radius:
                    enemy.take_damage(self.damage)
            self.current_cooldown = self.cooldown
        else:
            self.current_cooldown -= 1

    def draw(self, screen, x, y):
        if self.current_cooldown <= 0:
            color = (200, 200, 200)  # Light gray when active
        else:
            color = (100, 100, 100)  # Darker gray when on cooldown
        pygame.draw.circle(screen, color, (x, y), self.radius, 2)
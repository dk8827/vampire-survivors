import pygame
from weapon import Knife

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)
        self.speed = 5
        self.experience = 0
        self.level = 1
        self.weapons = [Knife("Knife", 1)]  # Always start with the knife
        self.powerups = []
        self.max_hp = 100
        self.hp = self.max_hp

    def move(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        self.rect.clamp_ip(pygame.display.get_surface().get_rect())

    def level_up(self):
        self.level += 1
        self.speed += 0.2
        self.max_hp += 10
        self.hp = self.max_hp  # Heal to full when leveling up

    def add_weapon(self, weapon):
        existing_weapon = next((w for w in self.weapons if w.name == weapon.name), None)
        if existing_weapon:
            existing_weapon.level_up()
        else:
            self.weapons.append(weapon)

    def add_powerup(self, powerup):
        existing_powerup = next((p for p in self.powerups if p.name == powerup.name), None)
        if existing_powerup:
            existing_powerup.level_up()
        else:
            self.powerups.append(powerup)
            powerup.apply(self)

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
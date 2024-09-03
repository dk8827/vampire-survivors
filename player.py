import pygame
from weapon import Knife

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load("player.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (40, 40))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)
        # ... rest of the initialization code ...
        self.speed = 5
        self.experience = 0
        self.level = 1
        self.weapons = [Knife("Knife", 1)]  # Always start with the knife
        self.powerups = []
        self.max_hp = 100
        self.hp = self.max_hp
        self.last_direction = pygame.math.Vector2(1, 0)  # Default to right
        self.facing_right = True

    def move(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        self.rect.clamp_ip(pygame.display.get_surface().get_rect())
        if dx != 0 or dy != 0:
            self.last_direction = pygame.math.Vector2(dx, dy).normalize()
        
        # Store the center before flipping
        center = self.rect.center
        
        # Flip the image based on movement direction
        if dx < 0 and self.facing_right:
            self.image = pygame.transform.flip(self.original_image, True, False)
            self.facing_right = False
        elif dx > 0 and not self.facing_right:
            self.image = self.original_image
            self.facing_right = True
        
        # Reset the rect and restore the center
        self.rect = self.image.get_rect()
        self.rect.center = center    
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
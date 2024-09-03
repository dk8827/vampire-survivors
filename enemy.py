import pygame
import random
import math
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("bat.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.rect.x = random.randint(0, screen.get_width() - self.rect.width)
        self.rect.y = random.choice([0, screen.get_height() - self.rect.height])
        self.speed = random.uniform(0.5, 2)
        self.hp = 1  # Default HP
        self.position = pygame.math.Vector2(self.rect.center)
        self.original_image = self.image.copy()
        self.hit_timer = 0
        self.hit_duration = 5

    def set_hp(self, base_hp):
        self.hp = base_hp

    def take_damage(self, amount):
        self.hp -= amount
        self.image = self.original_image.copy()
        self.image.fill((255, 255, 255), special_flags=pygame.BLEND_RGB_ADD)
        self.hit_timer = self.hit_duration
        if self.hp <= 0:
            self.kill()

    def update(self, player, enemies):
        # Move towards player
        direction = pygame.math.Vector2(player.rect.center) - self.position
        if direction.length() > 0:
            direction = direction.normalize()
        
        new_position = self.position + direction * self.speed

        # Collision with other enemies
        for other in enemies:
            if other != self:
                distance = self.position.distance_to(other.position)
                if distance < 20:  # 20 is the sum of radii (both enemies are 20x20)
                    overlap = 20 - distance
                    direction = (self.position - other.position).normalize()
                    new_position += direction * overlap / 2

        # Update position
        self.position = new_position
        self.rect.center = self.position

        # Keep enemy within screen bounds
        screen_rect = pygame.display.get_surface().get_rect()
        self.rect.clamp_ip(screen_rect)
        self.position = pygame.math.Vector2(self.rect.center)

        if self.hit_timer > 0:
            self.hit_timer -= 1
            if self.hit_timer == 0:
                self.image = self.original_image.copy()

        # ... rest of the update method ...
        pass  # This method is no longer needed        self.image.fill((255, 0, 0))  # Reset to original red color            pygame.time.set_timer(pygame.USEREVENT, 100)  # Reset color after 100ms            self.kill()
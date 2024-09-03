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
        self.hp = 10
        self.position = pygame.math.Vector2(self.rect.center)

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

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.kill()
        else:
            # Visual feedback for damage
            original_color = self.image.get_at((0, 0))
            self.image.fill((255, 100, 100))  # Flash red
            pygame.time.set_timer(pygame.USEREVENT, 100)  # Reset color after 100ms
            pygame.time.set_timer(pygame.USEREVENT + 1, 100)  # Custom event to reset color

    def reset_color(self):
        self.image.fill((255, 0, 0))  # Reset to original red color            pygame.time.set_timer(pygame.USEREVENT, 100)  # Reset color after 100ms            self.kill()
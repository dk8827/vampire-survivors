import pygame
import random
import math
class Enemy(pygame.sprite.Sprite):
    def __init__(self, base_hp):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.color = (255, 0, 0)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.rect.x = random.randint(0, screen.get_width() - self.rect.width)
        self.rect.y = random.choice([0, screen.get_height() - self.rect.height])
        self.speed = random.uniform(0.5, 2)
        self.hp = base_hp
        self.position = pygame.math.Vector2(self.rect.center)
        self.hit_timer = 0
        self.hit_duration = 5
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

        # Handle color reset
        if self.hit_timer > 0:
            self.hit_timer -= 1
            if self.hit_timer == 0:
                self.image.fill(self.color)  # Reset to original color

    def take_damage(self, amount):
        self.hp -= amount
        self.image.fill((255, 255, 255))  # Change color to white when hit
        self.hit_timer = self.hit_duration
        if self.hp <= 0:
            self.kill()

    def reset_color(self):
        pass  # This method is no longer needed        self.image.fill((255, 0, 0))  # Reset to original red color            pygame.time.set_timer(pygame.USEREVENT, 100)  # Reset color after 100ms            self.kill()
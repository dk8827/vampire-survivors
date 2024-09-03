import pygame
import random
from player import Player
from enemy import Enemy
from gem import Gem
from weapon import Weapon, Knife, Axe, Fireball, Garlic
from powerup import SpeedBoost, ArmorBoost, MagnetBoost
from ui import UI
from powerup import SpeedBoost, ArmorBoost, MagnetBoost
from ui import UI

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vampire Survivors Clone")

# Colors
BLACK = (0, 0, 0)

def get_random_upgrade(player):
    all_upgrades = [
        Knife("Knife", 1),
        Axe("Axe", 1),
        Fireball("Fireball", 1),
        Garlic("Garlic", 1),  # Add Garlic to possible upgrades
        SpeedBoost("Speed Boost", 1),
        ArmorBoost("Armor Boost", 1),
        MagnetBoost("Magnet Boost", 1)
    ]
    return random.sample([u for u in all_upgrades if not any(w.name == u.name for w in player.weapons + player.powerups)], 3)

def main():
    clock = pygame.time.Clock()
    player = Player()
    enemies = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    gems = pygame.sprite.Group()
    ui = UI()
    
    spawn_timer = 0
    shoot_timer = 0
    damage_cooldown = 0

    running = True
    leveling_up = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if leveling_up and event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    choice = event.key - pygame.K_1
                    upgrade = upgrade_options[choice]
                    if isinstance(upgrade, Weapon):
                        player.add_weapon(upgrade)
                    else:
                        player.add_powerup(upgrade)
                    leveling_up = False

        if not leveling_up:
            # Player movement
            keys = pygame.key.get_pressed()
            dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
            dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
            player.move(dx, dy)

            # Spawn enemies
            spawn_timer += 1
            if spawn_timer >= 60:  # Spawn every second
                enemies.add(Enemy())
                spawn_timer = 0

            # Auto-attack
            shoot_timer += 1
            if shoot_timer >= 30:  # Attack every half second
                for weapon in player.weapons:
                    if isinstance(weapon, Garlic):
                        # Damage enemies within Garlic's radius
                        for enemy in enemies:
                            if pygame.math.Vector2(player.rect.center).distance_to(enemy.rect.center) <= weapon.radius:
                                enemy.take_damage(weapon.damage)
                    else:
                        weapon.attack(player.rect.centerx, player.rect.centery, projectiles)
                shoot_timer = 0

            # Update
            enemies.update(player)
            projectiles.update()

            # Collision detection
            for enemy in pygame.sprite.groupcollide(enemies, projectiles, True, True):
                if random.random() < 0.3:  # 30% chance to drop a gem
                    gems.add(Gem(enemy.rect.centerx, enemy.rect.centery))

            # Player-enemy collision
            if damage_cooldown == 0:
                for enemy in pygame.sprite.spritecollide(player, enemies, False):
                    player.take_damage(10)
                    damage_cooldown = 30  # Set cooldown to half a second (30 frames)
            else:
                damage_cooldown -= 1

            # Collect gems
            for gem in pygame.sprite.spritecollide(player, gems, True):
                player.experience += 1
                if player.experience >= player.level * 5:
                    player.level_up()
                    player.experience = 0
                    leveling_up = True
                    upgrade_options = get_random_upgrade(player)

            # Draw
            screen.fill(BLACK)
            screen.blit(player.image, player.rect)
            for weapon in player.weapons:
                if isinstance(weapon, Garlic):
                    weapon.draw(screen, player.rect.centerx, player.rect.centery)
            enemies.draw(screen)
            projectiles.draw(screen)
            gems.draw(screen)
            ui.draw(screen, player)
        else:
            ui.draw_level_up(screen, upgrade_options)

        pygame.display.flip()
        clock.tick(60)

        # Check for game over
        if player.hp <= 0:
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()

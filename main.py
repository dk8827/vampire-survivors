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
def spawn_enemy(enemies):
    new_enemy = Enemy()
    collision = True
    attempts = 0
    while collision and attempts < 100:
        collision = False
        for enemy in enemies:
            if new_enemy.rect.colliderect(enemy.rect):
                collision = True
                new_enemy.rect.x = random.randint(0, WIDTH - new_enemy.rect.width)
                new_enemy.rect.y = random.choice([0, HEIGHT - new_enemy.rect.height])
                new_enemy.position = pygame.math.Vector2(new_enemy.rect.center)
                break
        attempts += 1
    if not collision:
        enemies.add(new_enemy)

def main():
    clock = pygame.time.Clock()
    player = Player()
    enemies = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    gems = pygame.sprite.Group()
    ui = UI()
    
    spawn_timer = 0

    running = True
    leveling_up = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.USEREVENT + 1:
                for enemy in enemies:
                    enemy.reset_color()
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
                spawn_enemy(enemies)
                spawn_timer = 0

            # Weapon attacks
            for weapon in player.weapons:
                if isinstance(weapon, Garlic):
                    weapon.attack(player.rect.centerx, player.rect.centery, projectiles, enemies)
                else:
                    weapon.attack(player.rect.centerx, player.rect.centery, projectiles)

            # Update
            enemies.update(player, enemies)
            projectiles.update()

            # Collision detection
            for enemy in pygame.sprite.groupcollide(enemies, projectiles, False, True):
                enemy.take_damage(1)  # Assume each projectile deals 1 damage
                if enemy.hp <= 0:
                    if random.random() < 0.3:  # 30% chance to drop a gem
                        gems.add(Gem(enemy.rect.centerx, enemy.rect.centery))
                    enemy.kill()

            # Add this block for player-enemy collision
            for enemy in pygame.sprite.spritecollide(player, enemies, False):
                player.take_damage(1)  # Assume each enemy deals 1 damage per frame
                if player.hp <= 0:
                    running = False  # End the game if player's HP reaches 0

            # Collect gems
            for gem in pygame.sprite.spritecollide(player, gems, True):
                player.experience += 1
                if player.experience >= player.level * 5:
                    player.level_up()
                    player.experience = 0
                    leveling_up = True
                    upgrade_options = get_random_upgrade(player)

            # Draw
            screen.fill((0, 0, 0))  # Black background
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
    


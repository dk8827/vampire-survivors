import pygame

class UI:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen, player):
        level_text = self.font.render(f"Level: {player.level}", True, (255, 255, 255))
        exp_text = self.font.render(f"EXP: {player.experience}/{player.level * 5}", True, (255, 255, 255))
        hp_text = self.font.render(f"HP: {player.hp}/{player.max_hp}", True, (255, 255, 255))
        screen.blit(level_text, (10, 10))
        screen.blit(exp_text, (10, 50))
        screen.blit(hp_text, (10, 90))

        # Draw HP bar
        bar_width = 200
        bar_height = 20
        fill_width = int((player.hp / player.max_hp) * bar_width)
        pygame.draw.rect(screen, (255, 0, 0), (10, 130, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (10, 130, fill_width, bar_height))

    def draw_level_up(self, screen, options):
        screen.fill((0, 0, 0, 128))
        title = self.font.render("Level Up! Choose an upgrade:", True, (255, 255, 255))
        screen.blit(title, (200, 150))

        for i, option in enumerate(options):
            text = self.font.render(f"{i+1}. {option.name} (Level {option.level})", True, (255, 255, 255))
            screen.blit(text, (220, 200 + i * 40))

        pygame.display.flip()

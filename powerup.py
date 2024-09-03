class Powerup:
    def __init__(self, name, level):
        self.name = name
        self.level = level

    def level_up(self):
        self.level += 1

    def apply(self, player):
        pass

class SpeedBoost(Powerup):
    def apply(self, player):
        player.speed += self.level * 0.5

class ArmorBoost(Powerup):
    def apply(self, player):
        # Implement armor logic here
        pass

class MagnetBoost(Powerup):
    def apply(self, player):
        # Implement magnet logic here
        pass

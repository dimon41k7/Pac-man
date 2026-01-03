import pygame
from character import *
class Lives:
    def __init__(self, lives=3):
        self.lives = lives

    @property
    def is_alive(self):
        return self.lives > 0

class Player(Character, Lives):
    def __init__(self, x: int, y: int, name):
        Character.__init__(self, x, y)
        Lives.__init__(self, lives=3)
        self.direction = "right"
        self.name = name

        self.steps = 0 
        self.collected = 0 
        self.invincible = 0

    def add_step(self):
        self.steps += 1

    def collect(self):
        self.collected += 1
        
    def add_life(self):
        self.lives += 1

    def lose_life(self):
        now = pygame.time.get_ticks()
        if now < self.invincible:
            return
        self.lives -= 1
        self.invincible = now + 1500

    def __str__(self):
        return f"Гравець {self.name}: {self.collected} очок"


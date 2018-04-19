import pygame
from utils import *

class Bullet:

    def __init__(self, game, pos=[0,0], size=3, vel=(0,0), damage=10, color=(100,100,100), name="Bullet"):
    
        self.game = game
        self.name = name
        self.color = color
        self.pos = pos
        self.size = size
        self.rect = pygame.Rect(pos[0], pos[1], self.size, self.size)
        
        self.vel = vel
        self.damage = damage
        
    def update(self, now):
    
        self.pos = add(self.pos, self.vel)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size, self.size)
    
    def draw(self):
    
        # pygame.draw.rect(self.game.screen, self.color, self.rect)
        pygame.draw.circle(self.game.screen, self.color, self.rect.center, self.size)
        
    def __str__():
    
        return self.name

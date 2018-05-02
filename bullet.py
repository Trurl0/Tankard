import pygame
from utils import *

class Bullet:

    def __init__(self, game, pos=[0,0], size=3, vel=(0,0), damage=10, color=(50,50,50), name="Bullet"):
    
        self.game = game
        self.name = name
        self.color = color
        self.pos = pos
        self.size = size
        self.rect = pygame.Rect(pos[0], pos[1], self.size, self.size)
        
        self.vel = vel
        self.damage = damage
        
    def update(self, now):
    
        self.pos = add_vector(self.pos, self.vel)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size, self.size)
    
    def check_collisions(self):
    
        for coll in self.game.tanks:
            if self.rect.colliderect(coll):
                try:
                    coll.life -= self.damage
                    
                    self.game.bullets.remove(self)
                    
                except Exception as e:
                    pass # print(e)
                    
        for coll in self.game.walls:
            if self.rect.colliderect(coll):
                try:                    
                    self.game.bullets.remove(self)
                except Exception as e:
                    pass # print(e)
    
    def draw(self):
    
        pygame.draw.circle(self.game.screen, self.color, self.rect.center, self.size)
        
    def __str__():
    
        return self.name

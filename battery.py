import pygame

class Battery:

    def __init__(self, game, pos=[0,0], energy=10, size=10, color=(0,255,0), name="Battery"):
    
        self.game = game
        self.name = name
        self.color = color
        self.size = size
        self.rect = pygame.Rect(pos[0], pos[1], size, size)
        
        self.energy = energy
        
    def draw(self):
    
        pygame.draw.rect(self.game.screen, self.color, self.rect)
        
    def __str__():
    
        return self.name

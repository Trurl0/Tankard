import pygame

class Battery:

    def __init__(self, game, pos=[0,0], energy=10, size=[10,10], color=(10,200,10), name="Battery"):
    
        self.game = game
        self.name = name
        self.color = color
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        
        self.energy = energy
        
    def draw(self):
    
        pygame.draw.rect(self.game.screen, self.color, self.rect)
        
    def __str__():
    
        return self.name

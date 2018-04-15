import pygame

class Wall:

    def __init__(self, game, pos=[0,0], size=[0,0], color=(150,150,150), name="Wall"):
    
        self.game = game
        self.name = name
        self.color = color
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        
    def draw(self):
    
        pygame.draw.rect(self.game.screen, self.color, self.rect)
        
    def __str__():
    
        return self.name

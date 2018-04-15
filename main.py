import pygame,random
import math
import random
from wall import Wall
from tank import Tank
from utils import *

class Game:
    def __init__(self):
    
        pygame.init()
        pygame.display.set_caption('Tanks')
        self.screen_width=600
        self.screen_height=400
        self.bg_color = WHITE
        self.screen=pygame.display.set_mode([self.screen_width, self.screen_height])
        
        self.last = pygame.time.get_ticks()
        self.clock = pygame.time.Clock()

        self.walls = []
        self.tanks = []
        
        self.running = True
      
    def msg(self, text, x, y, color, size):
        """Write a string to self.screen"""
        self.font = pygame.font.SysFont('georgia', size, bold=1)
        msgtxt = self.font.render(text, 1, color)
        msgrect = msgtxt.get_rect()
        msgrect.center = x/2, y/2
        self.screen.blit(msgtxt, (msgrect.center))
      
    def pause(self):
        """Pause the game"""
        wait = True
        while wait:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   pygame.quit()
                   quit()
                if event.type == pygame.KEYDOWN:
                   if event.key == pygame.K_RETURN:
                      wait = 0
                      print("RETURN PRESSED")
            self.msg("Paused", self.screen_width-150, self.screen_height-100, RED, 40)
            pygame.display.flip()
        
        #Clear txt
        self.screen.fill(self.bg_color)
         
    def new(self):
        """Reset all components"""
        self.tanks = []
        self.walls = []
        
        # Background
        self.screen.fill(self.bg_color)
        
        # Tanks
        # for i in range(10):
            # self.tanks.append(Tank("MK"+str(i), (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)), [random.randint(20, self.screen_width-20), random.randint(20, self.screen_height-20)]))
        
        t1 = Tank(self, "MK1", BLUE, [200, 300])
        t2 = Tank(self, "MK2", RED, [400, 100])
        self.tanks.append(t1)
        self.tanks.append(t2)
        
        # Walls
        self.walls.append(Wall(self, [0, 0], [10, self.screen_height], BLACK))
        self.walls.append(Wall(self, [0, 0], [self.screen_width, 10], BLACK))
        self.walls.append(Wall(self, [self.screen_width-10, 0], [10, self.screen_height], BLACK))
        self.walls.append(Wall(self, [0, self.screen_height-10], [self.screen_width, 10], BLACK))
       
        # Obstacles
        self.walls.append(Wall(self, [300, 50], [10, 100], BLACK, name="Wall1"))
        self.walls.append(Wall(self, [305, 155], [10, 50], BLACK, name="Wall2"))
        self.walls.append(Wall(self, [310, 155], [10, 50], BLACK, name="Wall2b"))
        self.walls.append(Wall(self, [310, 205], [10, 50], BLACK, name="Wall3"))
        self.walls.append(Wall(self, [315, 255], [10, 50], BLACK, name="Wall4"))
        self.walls.append(Wall(self, [320, 305], [10, 100], BLACK, name="Wall5"))
        # self.walls.append(Wall([320, 50], [10, 600], BLACK))
        # self.walls.append(Wall([350, 50], [10, 600], BLACK))
        # self.walls.append(Wall([400, 50], [10, 600], BLACK))
        
    def run(self):
      while self.running:
         self.event()
         self.update()
         self.draw()
         pygame.display.flip()
      
    def event(self):
          for event in pygame.event.get():
             if event.type==pygame.QUIT:
                self.running = False
                pygame.quit()
                quit()
             if event.type==pygame.KEYDOWN:
                   if event.key==pygame.K_RETURN:
                      self.pause()

    def update(self):
        """Make all self.screen elements update themselves"""
        # clock.tick(600)
        now = pygame.time.get_ticks()
        
        # Move actors
        for t in self.tanks:
            t.update(now)
            
            # Check stuff
            self.check_collisions(t)
        
    def check_collisions(self, t):
        # Check collisions
        
        for c in self.walls+self.tanks:
            if c is not t:
                if t.rect.colliderect(c):
                    
                    intersection = t.rect.clip(c)
                    push = normalize(sub(t.pos, intersection))
                    # print( str(t.rect.center) +", "+ str(intersection.center) +", "+ str(push))
                    
                    t.pos[0] += push[0]
                    t.pos[1] += push[1]
                    
                    # Stop after collision?
                    t.vel = [0, 0]
                    t.acc = [0, 0]

    def draw(self):
        """Make all self.screen elements draw themselves"""
        
        # Background
        self.screen.fill(self.bg_color)
        
        # Everything
        for a in self.walls+self.tanks:
            a.draw()
            
    def game_over(self):
        wait = True
        self.gover=1
        while wait:
             for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   pygame.quit()
                   quit()
                if event.type == pygame.KEYDOWN:
                   if event.key == pygame.K_RETURN:
                      wait = False
             self.msg("Game Over", self.screen_width-150, self.screen_height-100, red, 40)
             self.msg("Press Enter to Play Again", self.screen_width-545, self.screen_height+200, red, 40)
             pygame.display.flip()
        self.new()
     
if __name__=="__main__":

    g = Game()
    g.new()
    g.run()

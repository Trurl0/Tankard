import pygame,random
import math
import random
from wall import Wall
from tank import Tank
from battery import Battery
from bullet import Bullet
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
        """Reset all components for a new game"""
        
        self.tanks = []
        self.walls = []
        self.batteries = []
        self.bullets = []
        
        # Background
        self.screen.fill(self.bg_color)
        
        # Tanks        
        t1 = Tank(self, "MK1", "player1.py", BLUE, [200, 300])
        t2 = Tank(self, "MK2", "player2.py", RED, [400, 100])
        self.tanks.append(t1)
        self.tanks.append(t2)
        
        # Walls
        self.walls.append(Wall(self, [0, 0], [10, self.screen_height], BLACK))
        self.walls.append(Wall(self, [0, 0], [self.screen_width, 10], BLACK))
        self.walls.append(Wall(self, [self.screen_width-10, 0], [10, self.screen_height], BLACK))
        self.walls.append(Wall(self, [0, self.screen_height-10], [self.screen_width, 10], BLACK))
       
        # Obstacles
        self.walls.append(Wall(self, [300, 50], [10, 100], BLACK, name="Wall1"))
        # self.walls.append(Wall(self, [305, 155], [10, 50], BLACK, name="Wall2"))
        self.walls.append(Wall(self, [310, 300], [10, 50], BLACK, name="Wall3"))
        
        for i in range(5):
            self.batteries.append(Battery(self, [random.randint(50, self.screen_width-50), random.randint(50, self.screen_height-50)], name="Battery"))
            
        for i in range(10):
             self.bullets.append(Bullet(self, [random.randint(50, self.screen_width-50), random.randint(50, self.screen_height-50)], vel=(0.1,0), name="Bullet"))
        
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
            self.check_tank_collisions(t)
            
        for b in self.bullets:
            b.update(now)
            
            # Check stuff
            self.check_bullet_collisions(b)
        
    def check_bullet_collisions(self, bullet):
    
        for coll in self.tanks:
            if bullet.rect.colliderect(coll):
    
                    coll.life -= bullet.damage
                    
                    self.bullets.remove(bullet)
                    
        for coll in self.walls:
            if bullet.rect.colliderect(coll):
                
                self.bullets.remove(bullet)
    
    def check_tank_collisions(self, tank):
        # Check collisions, this could be done in each class...
        
        for coll in self.walls+self.tanks:
            if coll is not tank:
                if tank.rect.colliderect(coll):
                    
                    intersection = tank.rect.clip(coll)
                    push = mult(normalize(sub(tank.pos, intersection)), 2)
                    
                    tank.pos = add(push, tank.pos)
                    
                    # Stop after collision?
                    tank.vel = (0, 0)
                    tank.acc = (0, 0)
                    
        for battery in self.batteries:
            if tank.rect.colliderect(battery):
            
                tank.life += battery.energy
                
                self.batteries.remove(battery)
                    

    def draw(self):
        """Make all self.screen elements draw themselves"""
        
        # Background
        self.screen.fill(self.bg_color)
        
        # Everything
        for a in self.batteries+self.walls+self.tanks+self.bullets:
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

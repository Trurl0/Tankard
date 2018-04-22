'''
<Tankard: Program your troops AI>
Copyright (C) 2017 Trurl 
<m.xanxez@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import pygame,random
import math
import random
import os
from wall import Wall
from tank import Tank
from battery import Battery
from bullet import Bullet
from create_player import check_player_file
from utils import *

class Game:
    def __init__(self):
    
        pygame.init()
        pygame.display.set_caption('Tanks')
        # DISPLAYSURF = pygame.display.set_mode((400, 300), pygame.FULLSCREEN)
        
        self.screen_width=1000
        self.screen_height=600
        self.bg_color = (160, 175, 160)
        
        self.number_of_players = 2
        self.tanks_per_team = 5
        self.player1_input = "player1.py"
        self.player2_input = "player1.py"
        self.player1_color = BLUE
        self.player2_color = RED
        self.player1_color = (40,40,200)
        self.player2_color = (200,40,40)
        
        self.number_of_obstacles = 8
        self.number_of_batteries = 10
        
        self.max_speed = 0.3
        self.gun_cooldown = 500
        self.bullet_damage = 10
        
        self.debug = 0
        self.fullscreen = 0
        
        try:
            self.config("config.ini")
        except Exception as e:
            print(e)
            
        self.screen=pygame.display.set_mode([self.screen_width, self.screen_height])
        # self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        
        self.last = pygame.time.get_ticks()
        self.clock = pygame.time.Clock()

        self.walls = []
        self.tanks = []
        
        self.running = True
    
    def config(self, filename):
    
        if not os.path.exists(filename):
             with open(filename, 'w') as f:
                f.write("width = 1000\nheight = 600\nbackground_color = (160, 175, 160)\nplayers = 2\ntanks_per_team = 5\nplayer1 = player1.py\nplayer2 = player2.py\nnumber_of_obstacles = 6\nnumber_of_batteries = 10\ngun_cooldown = 4\nbullet_damage = 20\ndebug = 0")

        with open(filename, "r") as f:
            for line in f.readlines():
            
                if "width" in line:
                    self.screen_width=int(line.split("=")[-1].strip())
                    
                if "height" in line:
                    self.screen_height=int(line.split("=")[-1].strip())
                    
                if "background_color" in line:
                    try:
                        tuple_str = line.split("=")[-1].strip()
                        r = int(tuple_str.split("(")[1].split(",")[0].strip())
                        g = int(tuple_str.split("(")[1].split(",")[1].strip())
                        b = int(tuple_str.split(",")[-1].split(")")[0].strip())
                        self.bg_color= (r,g,b)
                    except Exception as e:
                        print(e)
                        
                if "players" in line:
                    self.number_of_players=int(line.split("=")[-1].strip())
                    
                if "tanks_per_team" in line:
                    self.tanks_per_team=int(line.split("=")[-1].strip())
                    
                if "player1" in line:
                    self.player1_input=line.split("=")[-1].strip()
                    # Create input file if does not exists
                    check_player_file(self.player1_input)
                    
                if "player2" in line:
                    self.player2_input=line.split("=")[-1].strip()
                    # Create input file if does not exists
                    check_player_file(self.player2_input)
                    
                if "number_of_obstacles" in line:
                    self.number_of_obstacles=int(line.split("=")[-1].strip())
                    
                if "number_of_batteries" in line:
                    self.number_of_batteries=int(line.split("=")[-1].strip())
                    
                if "max_speed" in line:
                    self.max_speed=int(line.split("=")[-1].strip())
                    
                if "gun_cooldown" in line:
                    self.gun_cooldown=100*int(line.split("=")[-1].strip())
                    
                if "bullet_damage" in line:
                    self.bullet_damage=int(line.split("=")[-1].strip())
                    
                if "debug" in line:
                    self.debug=int(line.split("=")[-1].strip())
                    
    def new(self):
        """Reset all components for a new game"""
        
        try:
            self.config("config.ini")
        except Exception as e:
            print(e)
            
        self.tanks = []
        self.walls = []
        self.batteries = []
        self.bullets = []
        
        # Background
        self.screen.fill(self.bg_color)
        
        # Walls
        self.walls.append(Wall(self, [0, 0], [10, self.screen_height], BLACK))
        self.walls.append(Wall(self, [0, 0], [self.screen_width, 10], BLACK))
        self.walls.append(Wall(self, [self.screen_width-10, 0], [10, self.screen_height], BLACK))
        self.walls.append(Wall(self, [0, self.screen_height-10], [self.screen_width, 10], BLACK))
       
        # Obstacles
        obstacles_color = (60, 50, 50)
        for i in range(self.number_of_obstacles):
            self.walls.append(Wall(self, [random.randint(self.screen_width*0.05, self.screen_width*0.95), random.randint(self.screen_height*0.05, self.screen_height*0.95)], [random.randint(self.screen_width*0.03,self.screen_width*0.2), random.randint(self.screen_height*0.03,self.screen_height*0.2)], obstacles_color, name="Wall"+str(i+1)))
        
        # Batteries
        batteries_color = (60, 50, 50)
        for i in range(self.number_of_batteries):
            battery_is_ok = False
            while not battery_is_ok:            
                check_coll = False
                battery = Battery(self, [random.randint(50, self.screen_width-50), random.randint(50, self.screen_height-50)], energy=self.bullet_damage, name="Battery"+str(i+1))
                for wall in self.walls:
                    if battery.rect.colliderect(wall):
                        # print("Coll: "+battery.name+", "+wall.name)
                        check_coll = True
                        break
                if not check_coll:
                    battery_is_ok = True
                    self.batteries.append(battery)
            
        # Tanks
        for i in range(self.tanks_per_team):
        
            self.tanks.append(Tank(self, "P1-"+str(i+1), team=1, input_file=self.player1_input, color=self.player1_color, pos=[self.screen_width*0.1, self.screen_height*0.1*(i+1)], max_speed=self.max_speed, gun_damage=self.bullet_damage, gun_max_cooldown=self.gun_cooldown))
            
            self.tanks.append(Tank(self, "P2-"+str(i+1), team=2, input_file=self.player2_input, color=self.player2_color, pos=[self.screen_width*0.9, self.screen_height*0.1*(i+1)], max_speed=self.max_speed, gun_damage=self.bullet_damage, gun_max_cooldown=self.gun_cooldown))
        
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
                   if event.key in [pygame.K_RETURN, pygame.K_ESCAPE, pygame.K_SPACE]:
                      self.pause()

    def update(self):
        """Make all screen elements update themselves"""
        
        # Used to manage how fast the screen updates
        self.clock.tick(500)
        now = pygame.time.get_ticks()
        
        # Move actors
        for t in self.tanks + self.bullets:
            t.update(now)
            t.check_collisions()
        
        self.check_game_over()
        
    def draw(self):
        """Make all screen elements draw themselves"""
        
        # Background
        self.screen.fill(self.bg_color)
        
        # Everything
        for a in self.batteries + self.walls + self.tanks + self.bullets:
            a.draw()
            
    def check_game_over(self):
        """Check if there is only one team remaining"""
        
        team_alive = None
        team_color = GREEN
        game_over = True
        for t in self.tanks:
            if team_alive is None:
                team_alive = t.team
                team_color = t.color
                
            elif team_alive != t.team:
                # At least two teams alive
                game_over = False
                break
                
        if game_over:
            self.game_over(team_alive, team_color)
        
    def pause(self):
        """Pause the game"""
        
        wait = True
        while wait:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        wait = False
                        pygame.quit()
                        quit()
                    if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                        wait = False
                    if event.key == pygame.K_r:
                        wait = False
                        self.new()
            self.msg("Paused", self.screen_width*0.80, self.screen_height*0.60, WHITE, 60)
            self.msg("Press Enter to resume", self.screen_width*0.81, self.screen_height*0.90, WHITE, 20)
            self.msg("Press R to re-start", self.screen_width*0.85, self.screen_height*1.00, WHITE, 20)
            self.msg("Press Esc to exit", self.screen_width*0.87, self.screen_height*1.1, WHITE, 20)
            pygame.display.flip()
        
        #Clear txt
        self.screen.fill(self.bg_color)
         
    def game_over(self, team_alive, color):
        wait = True
        while wait:
             for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   pygame.quit()
                   quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        wait = False
                    if event.key == pygame.K_ESCAPE:
                        wait = False
                        pygame.quit()
                        quit()
             self.msg("Winner: Team "+str(team_alive)+"!", self.screen_width*0.48, self.screen_height*0.60, color, 60)
             self.msg("Press Enter to Play Again", self.screen_width*0.73, self.screen_height*1.0, color, 20)
             self.msg("Press Esc to exit", self.screen_width*0.83, self.screen_height*1.10, color, 20)
             pygame.display.flip()
        self.new()
     
    def msg(self, text, x, y, color, size):
        """Write a string to self.screen"""
        self.font = pygame.font.SysFont('georgia', size, bold=1)
        msgtxt = self.font.render(text, 1, color)
        msgrect = msgtxt.get_rect()
        msgrect.center = x/2, y/2
        self.screen.blit(msgtxt, (msgrect.center))
      
if __name__=="__main__":

    g = Game()
    g.new()
    g.run()

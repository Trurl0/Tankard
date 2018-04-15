import pygame,random
import math
import random
from utils import *


class Tank():
    def __init__(self, game, name, color=(255,0,0), pos=[0,0], size=20, max_speed=0.1, turret_speed=0.001, gun_max_cooldown=2000, shoot_range=1000):
        
        self.game = game
        self.name = name
        self.color = color
        
        # Body
        self.pos = pos
        self.size = size
        self.rect = pygame.Rect(pos[0], pos[1], size, size)
        
        # Movement
        self.vel = [0, 0]
        self.acc = [0, 0]
        self.max_speed = max_speed
        
        # Gun
        self.gun_size = 15
        self.gun_dir = [0, -1]
        self.gun_target = [0, -1]
        self.turret_speed = turret_speed
        self.shoot_range = shoot_range
        self.gun_max_cooldown = gun_max_cooldown
        self.gun_last_cooldown = gun_max_cooldown
        self.shoor_order = False
      
    def update(self, now):
        """Update tank state with player input"""
        
        """Here goes the player logic"""
        """Here goes the player logic"""
        """Here goes the player logic"""
        
        # self.acc = [i+random.uniform(-0.01, 0.01) for i in self.acc]
        self.gun_target = normalize(sub([400, 100], self.pos))
        if self.name == "MK1":
            self.shoor_order = True
        
        """Here ends the player logic"""
        """Here ends the player logic"""
        """Here ends the player logic"""
        
        # SUbstract friction, add acceleration
        friction = 0.9
        self.vel = mult(self.vel, friction)
        self.vel = add(self.vel, self.acc)
        # Cap at max speed
        if magnitude(self.vel) > self.max_speed:
            self.vel = [i*self.max_speed for i in normalize(self.vel)]
        
        # Move tank
        self.pos = add(self.pos, self.vel)
        # Update Rect (needs to be independant for float precission)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size, self.size)
        
        # Move gun to target
        self.gun_dir = normalize(add(self.gun_dir, mult(sub(self.gun_target, self.gun_dir), self.turret_speed)))
        
        # Shoot
        if self.gun_last_cooldown > 0:
            self.gun_last_cooldown -= 1
        elif self.shoor_order:
            self.gun_last_cooldown = self.gun_max_cooldown
            self.shoor_order = False
            
            hits = raycast(self.rect.center, self.gun_dir, self.game.tanks+self.game.walls, self.shoot_range, first_only=False, ignore=None)
        
            for hit in hits:
                print(str(hit[0].name)+", "+str(hit[1]))
        
    def draw(self):
    
        # Body
        pygame.draw.rect(self.game.screen, self.color, self.rect)
        pygame.draw.circle(self.game.screen, GRAY, [int(i+(self.size/2)) for i in self.pos], int((self.size/2))-3)
        
        # Gun
        gun_center = [self.pos[0]+(self.size/2), self.pos[1]+(self.size/2)]
        gun_end = add(gun_center, mult(normalize(self.gun_dir), self.gun_size))
        pygame.draw.line(self.game.screen, GRAY, gun_center, gun_end, 5)
        
        # Shot
        if self.gun_last_cooldown > self.gun_max_cooldown-500:
            if self.gun_last_cooldown > self.gun_max_cooldown-100:
                shot_ini = gun_end
                shot_end = add(gun_center, mult(normalize(self.gun_dir), self.gun_size*3))
                shot_size = 10
            elif self.gun_last_cooldown > self.gun_max_cooldown-200:
                shot_ini = gun_end
                shot_end = add(gun_center, mult(normalize(self.gun_dir), self.gun_size*10))
                shot_size = 2
            elif self.gun_last_cooldown > self.gun_max_cooldown-300:
                shot_ini = gun_end
                shot_end = add(gun_center, mult(normalize(self.gun_dir), self.gun_size*10))
                shot_size = 2
            elif self.gun_last_cooldown > self.gun_max_cooldown-400:
                shot_ini = add(gun_center, mult(normalize(self.gun_dir), self.gun_size*10))
                shot_end = add(gun_center, mult(normalize(self.gun_dir), self.gun_size*20))
                shot_size = 1
            else:
                shot_ini = add(gun_center, mult(normalize(self.gun_dir), self.gun_size*20))
                shot_end = add(gun_center, mult(normalize(self.gun_dir), self.gun_size*30))
                shot_size = 1
            pygame.draw.line(self.game.screen, YELLOW, shot_ini,shot_end, shot_size)
    
    def __str__():
    
            return self.name

            
import pygame,random
import math
import random
from utils import *
from importlib import reload
from bullet import Bullet

class Tank():
    def __init__(self, game, name, input_file, color=RED, pos=(0,0), size=20, life=100, max_acc=0.00001, max_speed=0.1, turret_speed=0.011, gun_max_cooldown=2000, shoot_range=200, shoot_speed=0.2, gun_damage=10, sonar_range=400, sonar_max_cooldown=1000):
        
        self.input_file =  input_file
        self.input_function = "player_input"
        # self.player_input = getattr(__import__(self.input_file, fromlist=[self.input_function]), self.input_function)

        self.game = game
        
        self.name = name
        self.color = color
        
        self.life = life
        
        # Body
        self.pos = pos
        self.size = size
        self.rect = pygame.Rect(pos[0], pos[1], size, size)
        
        # Movement
        self.vel = (0, 0)
        self.acc = (0, 0)
        self.max_speed = max_speed
        self.max_acc = max_acc
        
        # Gun
        self.gun_damage = gun_damage
        self.turret_speed = turret_speed
        self.shoot_range = shoot_range
        self.shoot_speed = shoot_speed
        self.gun_max_cooldown = gun_max_cooldown
        self.gun_cooldown = gun_max_cooldown
        self.gun_size = 15
        self.gun_dir = (0, -1)
        self.gun_target = (0, -1)
        self.shoot_order = False
        
        # Sonar
        self.sonar_range = sonar_range
        self.sonar_max_cooldown = sonar_max_cooldown
        self.sonar_cooldown = sonar_max_cooldown
        self.sonar_reading = []
      
    def update(self, now):
        """Update tank state with player input"""
            
        if self.life <= 0:
            self.die()
        
        # Get sonar reading
        self.sonar_cooldown -= 1
        if self.sonar_cooldown <= 0:
            self.sonar_cooldown = self.sonar_max_cooldown
            self.sonar_reading = self.sonar()

            
            #----------Here goes the player logic----------#
        
            try:
                # Import player code
                # self.player_input = getattr(__import__(self.input_file, fromlist=[self.input_function]), self.input_function)
                exec(open(self.input_file, "r").read(), globals())
                self.player_input = player_input
                
                # Info to send to the player
                player_state = (self.rect.center, self.vel, self.life, self.gun_dir, self.gun_cooldown)
                
                # Use player code
                self.acc, self.gun_target, self.shoot_order = self.player_input(player_state, self.sonar_reading)

                # Checks and limitations
                if not isinstance(self.acc, tuple) or len(self.acc)!=2:
                    self.acc = (0, 0)

                else:
                    if magnitude(self.acc) > self.max_acc:
                        self.acc = mult(normalize(self.acc), self.max_acc)
                    
                if not isinstance(self.gun_target, tuple) or len(self.gun_target)!=2:
                    self.gun_target = (0, -1)
                else:
                    self.gun_target = normalize(self.gun_target)
                    
                if not isinstance(self.shoot_order, bool):
                    self.shoot_order = False
                        
            except:
                self.acc = (0, 0)
                self.gun_target = (0, 1)
                self.shoot_order = False
                
            #----------Here ends the player logic----------#

        
        # Substract friction, add acceleration
        friction = 0.9999
        self.vel = mult(self.vel, friction)
        self.vel = add(self.vel, self.acc)
        # Cap at max speed
        if magnitude(self.vel) > self.max_speed:
            self.vel = [i*self.max_speed for i in normalize(self.vel)]
        
        # Move tank
        self.pos = add(self.pos, self.vel)
        # Update Rect (needs to be independant for float precission)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size, self.size)
        
        # Orient gun to target
        self.gun_dir = normalize(add(self.gun_dir, mult(sub(self.gun_target, self.gun_dir), self.turret_speed)))
        
        # Shoot
        if self.gun_cooldown > 0:
            self.gun_cooldown -= 1
        elif self.shoot_order:
            self.gun_cooldown = self.gun_max_cooldown
            self.shoot_order = False
            
            self.game.bullets.append(Bullet(self.game, add(self.rect.center, mult(self.gun_dir, 20)), vel=mult(normalize(self.gun_dir), self.shoot_speed), name="Bullet"))
            
            # hits = raycast(self.rect.center, self.gun_dir, self.game.tanks+self.game.walls, self.shoot_range, first_only=True, ignore=self)
            # Hit first object
            # if hits:
                # try:
                    # hits[0].get_hit(self.gun_damage)
                # except Exception as e:
                    # pass
    
    def sonar(self):
        """Return Rect of game objects in distance"""
        
        reading = []
        for obj in self.game.batteries + self.game.walls + self.game.tanks:
            if obj is not self:
                dist = magnitude(sub(obj.rect.center, self.rect.center))
                if dist < self.sonar_range:
                    # print(obj.name+": "+str(dist))
                    reading.append((str(type(obj)), obj.name, obj.rect))
        return reading
    
    def get_hit(self, damage):
    
        self.life -= damage
        # print(self.name+": I'm hit! (life: "+str(self.life)+")")
    
    def die(self):
    
        self.game.tanks.remove(self)
                
    def draw(self):
    
        # Body
        pygame.draw.rect(self.game.screen, self.color, self.rect)
        pygame.draw.circle(self.game.screen, GRAY, self.rect.center, int((self.size/2))-3)
        
        # Gun
        gun_center = self.rect.center
        gun_end = add(gun_center, mult(normalize(self.gun_dir), self.gun_size))
        pygame.draw.line(self.game.screen, GRAY, gun_center, gun_end, 5)
        
        # Life
        pygame.draw.line(self.game.screen, RED, add(self.pos, (0,-10)),add(self.pos, (self.size,-10)), 5)
        pygame.draw.line(self.game.screen, GREEN, add(self.pos, (0,-10)),add(self.pos, (self.size*(self.life/100),-10)), 5)
        
        # Shot
        if self.gun_cooldown > self.gun_max_cooldown-500:
            if self.gun_cooldown > self.gun_max_cooldown-100:
                shot_ini = gun_end
                shot_end = add(gun_center, mult(normalize(self.gun_dir), self.gun_size*3))
                shot_size = 20
                pygame.draw.circle(self.game.screen, YELLOW, [int(i) for i in gun_end], 15)
                pygame.draw.line(self.game.screen, YELLOW, shot_ini,shot_end, shot_size)
                
            elif self.gun_cooldown > self.gun_max_cooldown-300:
                shot_ini = gun_end
                shot_end = add(gun_center, mult(normalize(self.gun_dir), self.gun_size*3))
                shot_size = 10
                pygame.draw.line(self.game.screen, YELLOW, shot_ini,shot_end, shot_size)
            else:
                shot_ini = gun_end
                shot_end = add(gun_center, mult(normalize(self.gun_dir), self.gun_size*2))
                shot_size = 10
                pygame.draw.line(self.game.screen, YELLOW, shot_ini,shot_end, shot_size)
            
            # elif self.gun_cooldown > self.gun_max_cooldown-300:
                # shot_ini = gun_end
                # shot_end = add(gun_center, mult(normalize(self.gun_dir), self.gun_size*10))
                # shot_size = 2
            # else:
                # shot_ini = add(gun_center, mult(normalize(self.gun_dir), self.gun_size*10))
                # shot_end = add(gun_center, mult(normalize(self.gun_dir), self.gun_size*20))
                # shot_size = 1
    
    def __str__():
    
        return self.name


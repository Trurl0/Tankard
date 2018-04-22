import pygame,random
import math
import random
from utils import *
from importlib import reload
from bullet import Bullet

class Tank():
    def __init__(self, game, name, team, input_file, color=RED, pos=(0,0), size=20, life=100, max_acc=0.002, max_speed=0.3, turret_speed=0.05, gun_max_cooldown=500, shoot_range=200, shoot_speed=1, gun_damage=10, sonar_range=400, sonar_max_cooldown=500):
        
        self.game = game
        
        self.input_file =  input_file
        self.input_function = "player_input"
        self.player_input_max_cooldown = 50
        self.player_input_cooldown = self.player_input_max_cooldown
        self.player_import_max_cooldown = 10
        self.player_import_cooldown = self.player_import_max_cooldown
        
        exec(open(self.input_file, "r").read(), globals())
        self.player_input = player_input
        
        self.name = name
        self.team = team
        self.color = color
        
        self.life = life
        self.is_dead = False
        self.dead_animation_counter = 0
        
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
        self.shoot_range = shoot_range  # Unused
        self.shoot_speed = shoot_speed
        self.gun_max_cooldown = gun_max_cooldown
        self.gun_cooldown = gun_max_cooldown/2
        self.gun_size = 15
        self.gun_dir = (0, -1)
        self.gun_target = (0, -1)
        self.shoot_order = False
        
        # Sonar
        self.sonar_range = sonar_range
        self.sonar_max_cooldown = sonar_max_cooldown
        self.sonar_cooldown = sonar_max_cooldown
        self.sonar_reading = []
        
        self.override_ai = False
        self.selected = False
      
    def update(self, now):
        """Update tank state with player input"""
            
        if self.life <= 0:
            self.die()
        
        if not self.is_dead:
            
          
            # Get sonar reading
            self.sonar_cooldown -= 1
            if self.sonar_cooldown <= 0:
                self.sonar_cooldown = self.sonar_max_cooldown
                self.sonar_reading = self.sonar()

                
            if not self.override_ai:
            #----------Here goes the player logic----------#
            
                self.player_input_cooldown -= 1
                if self.player_input_cooldown <= 0:
                    self.player_input_cooldown = self.player_input_max_cooldown
                    
                    try:

                        self.player_import_cooldown -= 1
                        if self.player_import_cooldown <= 0:
                            self.player_import_cooldown = self.player_import_max_cooldown
                            
                            # Import player code
                            exec(open(self.input_file, "r").read(), globals())
                            self.player_input = player_input
                                        
                        # Send info to player and use player code
                        self.acc, self.gun_target, self.shoot_order = self.player_input(self.game.screen_width, self.game.screen_height, self.rect.center, self.vel, self.life, self.gun_dir, self.gun_cooldown, self.team, self.sonar_reading)
                        
                        # Checks and limitations
                        if not isinstance(self.acc, tuple) or len(self.acc)!=2:
                            self.acc = (0, 0)
                            
                        if not isinstance(self.gun_target, tuple) or len(self.gun_target)!=2:
                            self.gun_target = (0, -1)
                            
                        if not isinstance(self.shoot_order, bool):
                            self.shoot_order = False
                            
                    except Exception as e:
                        print(e)
                        self.acc = (0, 0)
                        self.gun_target = (0, 1)
                        self.shoot_order = False
                    
            #----------Here ends the player logic----------#
            
            
            # Limit max acc
            if magnitude(self.acc) > self.max_acc:
                self.acc = mult(normalize(self.acc), self.max_acc)
                
            # Substract friction, add acceleration
            friction = 0.99
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
            self.gun_target = normalize(self.gun_target)
            self.gun_dir = normalize(add(self.gun_dir, mult(sub(self.gun_target, self.gun_dir), self.turret_speed)))
            
            # Shoot
            if self.gun_cooldown > 0:
                self.gun_cooldown -= 1
            elif self.shoot_order:
                self.gun_cooldown = self.gun_max_cooldown
                self.shoot_order = False
                
                self.game.bullets.append(Bullet(self.game, add(self.rect.center, mult(self.gun_dir, 20)), vel=mult(normalize(self.gun_dir), self.shoot_speed), damage=self.gun_damage))
                
                if self.game.sound:
                    self.game.gun_sound.play()
                
    def sonar(self):
        """Return Rect of game objects in distance"""
        
        reading = []
        for obj in self.game.batteries + self.game.walls + self.game.tanks:
            if obj is not self:
                dist = magnitude(sub(obj.rect.center, self.rect.center))
                if dist < self.sonar_range:
                    # print(obj.name+": "+str(dist))
                    if "Tank" in str(type(obj)):
                        obj_team = obj.team
                    else:
                        obj_team = 0
                    reading.append((str(type(obj)), obj.name, obj.rect, obj_team))
        return reading
    
    def get_hit(self, damage):
    
        self.life -= damage
        # print(self.name+": I'm hit! (life: "+str(self.life)+")")
    
    def die(self):
        
        self.is_dead = True
        
        if self.game.sound and self.dead_animation_counter == 0:
            self.game.failure_sound.play()
        
        self.dead_animation_counter += 1
        
        if self.dead_animation_counter > 150:
            self.game.tanks.remove(self)
             
    def check_collisions(self):
        
        # Walls
        for coll in self.game.walls:
            if coll is not self:
                if self.rect.colliderect(coll):
                    
                    intersection = self.rect.clip(coll)
                    if intersection == self.rect:
                        # Whole Tank inside obstacle
                        push = mult(normalize(sub(self.pos, coll.rect.center)), 2)
                    else:
                        push = mult(normalize(sub(self.pos, intersection)), 2)
                        
                    self.pos = add(push, self.pos)
                    
                    # Stop after collision?
                    self.vel = (0, 0)
                    self.acc = (0, 0)
        
        # Tanks        
        for coll in self.game.tanks:
            if coll is not self:
                if self.rect.colliderect(coll):

                    # Damage enemy (he will do the same to me)
                    if coll.team != self.team:
                        coll.life -= 1
                    
                    intersection = self.rect.clip(coll)
                    push = mult(normalize(sub(self.pos, intersection)), 2)
                    
                    self.pos = add(push, self.pos)
                    
                    # Stop after collision?
                    self.vel = (0, 0)
                    self.acc = (0, 0)
                    
        # Batteries
        for battery in self.game.batteries:
            if self.rect.colliderect(battery):
            
                self.life += battery.energy
                
                self.game.batteries.remove(battery)
                
                if self.game.sound:
                    self.game.battery_sound.play()
       
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
        if self.gun_cooldown > self.gun_max_cooldown-80:
            if self.gun_cooldown > self.gun_max_cooldown-20:
                shot_ini = gun_end
                shot_end = add(gun_center, mult(normalize(self.gun_dir), self.gun_size*3))
                shot_size = 20
                pygame.draw.circle(self.game.screen, YELLOW, [int(i) for i in gun_end], 20)
                pygame.draw.line(self.game.screen, YELLOW, shot_ini,shot_end, shot_size)
                
            elif self.gun_cooldown > self.gun_max_cooldown-60:
                shot_ini = gun_end
                shot_end = add(gun_center, mult(normalize(self.gun_dir), self.gun_size*3))
                shot_size = 10
                pygame.draw.line(self.game.screen, YELLOW, shot_ini,shot_end, shot_size)
            else:
                shot_ini = gun_end
                shot_end = add(gun_center, mult(normalize(self.gun_dir), self.gun_size*2))
                shot_size = 5
                pygame.draw.line(self.game.screen, YELLOW, shot_ini,shot_end, shot_size)
                
        # Draw explosions on death
        if self.is_dead:
            pygame.draw.circle(self.game.screen, random.choice([YELLOW,YELLOW, RED]), [int(i+random.randint(0,self.size*2)) for i in self.pos], random.randint(0,50))
                
        # Draw acceleration for debugging
        if self.game.debug:
            pygame.draw.line(self.game.screen, GREEN, self.rect.center, add(self.rect.center, mult(self.acc, 10000)), 1)
            
        # Draw name if selected
        if self.selected:
            self.game.msg(self.name, self.rect.center[0]*2-35, self.rect.center[1]*2+15, self.color, 15)
                
                
    def __str__():
    
        return self.name


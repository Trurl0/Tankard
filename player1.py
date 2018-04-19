from utils import *
import random
        

def player_input(tank_state, sonar_reading):
    
    tank_pos = tank_state[0]
    tank_vel = tank_state[1]
    tank_life = tank_state[2]
    tank_gun_dir = tank_state[3]
    tank_gun_cooldown = tank_state[4]
    
    acceleration = (0, 0)
    gun_dir = (0, 0)
    shoot_order = False
    
    #----------Your code here----------#
    
    # print("PLAYER 1")
    
    acceleration = (random.uniform(-0.01, 0.01), random.uniform(-0.01, 0.01))
    
    target_pos = None
    for obj in sonar_reading:
        obj_type = obj[0]
        obj_name = obj[1]
        obj_rect = obj[2]
        # print(obj_type)
        
        if "Battery" in obj_type:
            acceleration = normalize(sub(obj_rect.center, tank_pos))
            
        if "Tank" in obj_type:
            target_pos = obj_rect.center

    if target_pos is not None:
        gun_dir = normalize(sub(target_pos, tank_pos))
        shoot_order = True
    
    
    #----------Your code here----------#
    
    return acceleration, gun_dir, shoot_order
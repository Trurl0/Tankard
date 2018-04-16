

from utils import *
import random


def player_input(my_pos, sonar_reading):
    acceleration = (0, 0)
    gun_dir = (0, 0)
    shoot_order = False
    
    #----------Your code here----------#
    
    acceleration = (random.uniform(-0.01, 0.01), random.uniform(-0.01, 0.01))
    
    target = None
    target_pos = None
    for obj in sonar_reading:
        if "MK" in obj[1]:
            target = obj[1]
            target_pos = obj[2].center

    if target is not None:
        gun_dir = sub(target_pos, my_pos)
        shoot_order = True
    
    
    #----------Your code here----------#
    
    return acceleration, gun_dir, shoot_order
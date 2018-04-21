import os

def check_player_file(player_input_file):

    directory = os.path.dirname(player_input_file)

    if directory and not os.path.exists(directory):
        os.makedirs(directory)
        
    if not os.path.exists(player_input_file):
        with open(player_input_file, 'w') as f:
            f.write("\n\
from utils import *\n\
import random\n\
\n\
def player_input(screen_width, screen_height, tank_pos, tank_vel, tank_life, tank_gun_dir, tank_gun_cooldown, tank_team, sonar_reading):\n\
    \n\
    acceleration = (0, 0)\n\
    gun_dir = (0, 0)\n\
    shoot_order = False\n\
    \n\
    #----------Your code here----------#\n\
    \n\
    \n\
    \n\
    #----------Your code here----------#\n\
    \n\
    return acceleration, gun_dir, shoot_order\n\
    ")
        
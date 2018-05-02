import os

def check_player_file(player_input_file):

    directory = os.path.dirname(player_input_file)

    if directory and not os.path.exists(directory):
        os.makedirs(directory)
        
    if not os.path.exists(player_input_file):
        with open(player_input_file, 'w') as f:
            f.write("\n\
from utils import *\n\
\n\
\n\
def player_input(map_width, map_height, my_pos, my_vel, my_life, my_gun_dir, my_gun_cooldown, my_name, my_team, sonar_reading):\n\
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
        
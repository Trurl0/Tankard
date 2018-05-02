
from utils import *


def player_input(map_width, map_height, tank_pos, tank_vel, tank_life, tank_gun_dir, tank_gun_cooldown, tank_name, tank_team, sonar_reading):
        
    acceleration = (0, 0)
    gun_dir = (0, 0)
    shoot_order = False
    
    #----------Your code here----------#
    
    # Store wall rects
    walls = [obj[2] for obj in sonar_reading if "Wall" in obj[1]]
    batteries = [obj for obj in sonar_reading if "Battery" in obj[1]]
    enemy_tanks = [obj for obj in sonar_reading if ("Tank" in obj[0] and obj[3]!=tank_team)]
    friendly_tanks = [obj for obj in sonar_reading if "Tank" in obj[0] and obj[3]==tank_team]
    
    closest_battery = None
    closest_battery_dist = 10000
    for obj_type, obj_name, obj_rect, obj_team in batteries:
        dist =  magnitude(sub(obj_rect.center, tank_pos))
        if dist < closest_battery_dist:
            closest_battery_dist = dist
            closest_battery = obj_rect.center

    closest_enemy = None
    closest_enemy_dist = 10000
    for obj_type, obj_name, obj_rect, obj_team in enemy_tanks:
        dist =  magnitude(sub(obj_rect.center, tank_pos))
        if dist < closest_enemy_dist:
            gun_dir = sub(obj_rect.center, tank_pos)
            if check_clear_shot(tank_pos, gun_dir, tank_gun_dir, obj_rect.center, [obj[2] for obj in sonar_reading]):
                closest_enemy_dist = dist
                closest_enemy = obj_rect.center
            
    closest_friend = None
    closest_friend_dist = 10000
    for obj_type, obj_name, obj_rect, obj_team in friendly_tanks:
        dist =  magnitude(sub(obj_rect.center, tank_pos))
        if dist < 100:
            acceleration = add(acceleration, sub(tank_pos, obj_rect.center))
        elif dist > 200:
            acceleration = add(acceleration, sub(obj_rect.center, tank_pos))
            
    if closest_battery and closest_battery_dist < 200:
        # Go for battery
        acceleration = add(acceleration, sub(closest_battery, tank_pos))
        
    elif closest_enemy and closest_enemy_dist < 100:
        # Avoid enemy
        acceleration = add(acceleration, sub(tank_pos, closest_enemy))
        
    elif closest_enemy and closest_enemy_dist > 200:
        # Follow enemy
        acceleration = add(acceleration, sub(closest_enemy, tank_pos))
        
    elif closest_friend and closest_friend_dist < 80:
        # Follow enemy
        acceleration = add(acceleration, sub(closest_friend, tank_pos))
        
    else:
        acceleration = sub((map_width/2, map_height/2), tank_pos) 
        
        
    if closest_enemy is not None:
        gun_dir = sub(closest_enemy, tank_pos)
        if check_clear_shot(tank_pos, gun_dir, tank_gun_dir, closest_enemy, [obj[2] for obj in sonar_reading]):
            shoot_order = True
    
    
    acceleration = avoid_obstacles(tank_pos, None, acceleration, walls, 30)
    
    # Random movement for dodging
    random_acc = (random.uniform(-1, 1), random.uniform(-1, 1))
    acceleration = add(acceleration, mult(random_acc, 10))
    
    #----------Your code here----------#
    
    return acceleration, gun_dir, shoot_order

    
def avoid_obstacles(tank_pos, target, acceleration, obstacles, avoid_distance):
    # Raycast along acceleration vector, if something is close, rotate acceleration
    new_acceleration = acceleration
    acc_magnitude = magnitude(acceleration)
    
    hit = raycast(tank_pos, acceleration, obstacles, avoid_distance, first_only=True)
    if hit:
        if target is not None:
            target_dir = normalize(sub(target, tank_pos))
            obstacle_dir = normalize(sub(hit[0].center, tank_pos))
            new_acceleration = normalize(sub(target_dir, obstacle_dir))
        else:
            obstacle_dir = normalize(sub(hit[0].center, tank_pos))
            acceleration_dir = normalize(acceleration)
            new_acceleration = normalize(sub(acceleration_dir, obstacle_dir))
        
    return mult(new_acceleration, acc_magnitude)

    
def check_clear_shot(tank_pos, gun_dir, tank_gun_dir, closest_enemy, obstacles):
    
    shot_is_clear = False
    dist_to_enemy = magnitude(gun_dir)
    hit = raycast(tank_pos, tank_gun_dir, obstacles, dist_to_enemy, first_only=True)
    if hit:  # if no hits, what are we shooting at?
        if hit[0].center == closest_enemy:
            shot_is_clear = True
            
    return shot_is_clear
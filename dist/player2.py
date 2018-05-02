from utils import *
import random

def player_input(map_width, map_height, tank_pos, tank_vel, tank_life, tank_gun_dir, tank_gun_cooldown, tank_name, tank_team, sonar_reading):
        
    acceleration = (0, 0)
    gun_dir = (0, 0)
    shoot_order = False
    
    #----------Your code here----------#
    acceleration = sub_vector((map_width/2, map_height/2), tank_pos)   
    random_acc = (random.uniform(-1, 1), random.uniform(-1, 1))
    
    shoot_target = None
    closest_battery = None
    closest_battery_dist = 10000
    closest_enemy = None
    closest_enemy_dist = 10000
    
    avoid_allies_acc = (0, 0)
   
    # Store wall rects
    walls = [obj[2] for obj in sonar_reading if "Wall" in obj[1]]
    
    # Iterate sonar ignoring walls
    interesting_sonar_objects = [obj for obj in sonar_reading if "Wall" not in obj[1]]
    for obj_type, obj_name, obj_rect, obj_team in interesting_sonar_objects:
        
        if "Battery" in obj_type:
            dist =  magnitude(sub_vector(obj_rect.center, tank_pos))
            if dist < closest_battery_dist:
                closest_battery_dist = dist
                closest_battery = obj_rect.center
            
        # Do stuff to enemies
        if "Tank" in obj_type and obj_team!= tank_team:
            dist =  magnitude(sub_vector(obj_rect.center, tank_pos))
            if dist < closest_enemy_dist:
                closest_enemy_dist = dist
                closest_enemy = obj_rect.center
                
        # Avoid collision with allies
        if "Tank" in obj_type and obj_team == tank_team:
            dist =  magnitude(sub_vector(obj_rect.center, tank_pos))
            if dist <80:
                avoid_allies_acc = add_vector(avoid_allies_acc, mult_vector(sub_vector(tank_pos, obj_rect.center), 30))
            
    
    if closest_battery:
        acceleration = sub_vector(closest_battery, tank_pos)
    elif closest_enemy:
        if closest_enemy_dist < 100:
            acceleration = sub_vector(tank_pos, closest_enemy)
        elif closest_enemy_dist > 200:
            acceleration = sub_vector(closest_enemy, tank_pos)
            
    if closest_enemy is not None:
        gun_dir = sub_vector(closest_enemy, tank_pos)
        if check_clear_shot(tank_pos, gun_dir, tank_gun_dir, closest_enemy, [obj[2] for obj in sonar_reading]):
            shoot_order = True
    
    # Collision avoidance
    if closest_battery is not None:
        avoid_target = closest_battery
    else:
        avoid_target = closest_enemy
    # Raycast along acceleration vector, if something is close, rotate acceleration
    acceleration = avoid_obstacles(tank_pos, avoid_target, acceleration, walls, 30)
    
    # Avoid crashing with allies
    acceleration = add_vector(acceleration, avoid_allies_acc)
    
    # Random movement for dodging
    acceleration = add_vector(acceleration, mult_vector(random_acc, 10))
    
    #----------Your code here----------#
        
    return (acceleration, gun_dir, shoot_order)
    
    
def avoid_obstacles(tank_pos, target, acceleration, obstacles, avoid_distance):
    # Raycast along acceleration vector, if something is close, rotate acceleration
    new_acceleration = acceleration
    acc_magnitude = magnitude(acceleration)
    
    hit = raycast(tank_pos, acceleration, obstacles, avoid_distance, first_only=True)
    if hit:
        if target is not None:
            target_dir = normalize(sub_vector(target, tank_pos))
            obstacle_dir = normalize(sub_vector(hit[0].center, tank_pos))
            new_acceleration = normalize(sub_vector(target_dir, obstacle_dir))
        else:
            obstacle_dir = normalize(sub_vector(hit[0].center, tank_pos))
            acceleration_dir = normalize(acceleration)
            new_acceleration = normalize(sub_vector(acceleration_dir, obstacle_dir))
        
    return mult_vector(new_acceleration, acc_magnitude)
    
    
def check_clear_shot(tank_pos, gun_dir, tank_gun_dir, closest_enemy, obstacles):
    
    shot_is_clear = False
    dist_to_enemy = magnitude(gun_dir)
    hit = raycast(tank_pos, tank_gun_dir, obstacles, dist_to_enemy, first_only=True)
    if hit:  # if no hits, what are we shooting at?
        if hit[0].center == closest_enemy:
            shot_is_clear = True
            
    return shot_is_clear
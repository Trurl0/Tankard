from utils import *
import random

def player_input(screen_width, screen_height, tank_pos, tank_vel, tank_life, tank_gun_dir, tank_gun_cooldown, tank_team, sonar_reading):
        
    acceleration = (0, 0)
    gun_dir = (0, 0)
    shoot_order = False
    
    #----------Your code here----------#
    acceleration = sub((screen_width/2, screen_height/2), tank_pos)   
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
            dist =  magnitude(sub(obj_rect.center, tank_pos))
            if dist < closest_battery_dist:
                closest_battery_dist = dist
                closest_battery = obj_rect.center
            
        # Do stuff to enemies
        if "Tank" in obj_type and obj_team!= tank_team:
            dist =  magnitude(sub(obj_rect.center, tank_pos))
            if dist < closest_enemy_dist:
                closest_enemy_dist = dist
                closest_enemy = obj_rect.center
                
        # Avoid collision with allies
        if "Tank" in obj_type and obj_team == tank_team:
            dist =  magnitude(sub(obj_rect.center, tank_pos))
            if dist < 100:
                avoid_allies_acc = add(avoid_allies_acc, mult(sub(tank_pos, obj_rect.center), 10))
            
    
    if closest_battery:
        acceleration = sub(closest_battery, tank_pos)
    elif closest_enemy:
        if closest_enemy_dist < 100:
            acceleration = sub(tank_pos, closest_enemy)
        elif closest_enemy_dist > 200:
            acceleration = sub(closest_enemy, tank_pos)
            
    if closest_enemy is not None:
        gun_dir = sub(closest_enemy, tank_pos)
        if check_clear_shot(tank_pos, gun_dir, closest_enemy, [obj[2] for obj in sonar_reading]):
            shoot_order = True
    
    # Collision avoidance
    if closest_battery is not None:
        avoid_target = closest_battery
    else:
        avoid_target = closest_enemy
    # Raycast along acceleration vector, if something is close, rotate acceleration
    acceleration = avoid_obstacles(tank_pos, avoid_target, acceleration, walls, 30)
    
    # Avoid crashing with allies
    acceleration = add(acceleration, avoid_allies_acc)
    
    # Random movement for dodging
    acceleration = add(acceleration, mult(random_acc, 10))
    
    #----------Your code here----------#
        
    return acceleration, gun_dir, shoot_order
    
    
def avoid_obstacles(tank_pos, target, acceleration, obstacles, avoid_distance):

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
    
    
def check_clear_shot(tank_pos, gun_dir, closest_enemy, obstacles):
    
    shot_is_clear = False
    print(closest_enemy)
    dist_to_enemy = magnitude(gun_dir)
    hit = raycast(tank_pos, gun_dir, obstacles, dist_to_enemy, first_only=True)
    if hit:  # if no hits, what are we shooting at?
        if hit[0].center == closest_enemy:
            shot_is_clear = True
            
    return shot_is_clear
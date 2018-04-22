# Tankard
Top-down shooter without controls, the players code the behaviour of their units in real time. Built with Python3 and pygame.

A nice way of getting into programming with python and some violence.

## How to play:

The following variables in config.ini define the user input files:

```
player1 = player1.py
player2 = player2.py
```

Player1 units will use the function player_input() defined in player1.py to calculate its movement and shooting.

Player2 units will use the one defined in player2.py

#### The goal of the game is to program a smarter AI than your oponent (and murder its troops, of course).


## Input:

The input language is Python 3.6.5

The main function player_input() is called each game frame.
It has the following inputs:

```
screen_width, screen_height    # Map boundaries
tank_pos, tank_vel, tank_life  # Tank position, velocity and life. All vectors are tuples (x, y)
tank_gun_dir                   # Where the tank's cannon is pointing
tank_gun_cooldown              # Remaining time to be able to shoot again
tank_team                      # Tank faction
sonar_reading                  # List with all game objects detected by the tank within its range.
```   
And must return the following tuple:

```   
(acceleration, gun_dir, shoot_order)
acceleration                   # (x, y) Tank acceleration
gun_dir                        # (x, y) Where the cannon should be pointing, referenced from tank_pos
shoot_order                    # True or False, try to shoot when able
```   

### Reading the sonar
sonar_reading is a list of tuples with the following info:    
```   
obj_type                       # String with object class Tank, Wall, Battery... 
obj_name                       # Object name
obj_rect                       # Tuple with object coordinates (upper_left_x, upper_left_y, bottom_right_x, bottom_right_y). This is a pygame.Rect object, you can use obj_rect.center and such (https://www.pygame.org/docs/ref/rect.html)
obj_team                       # Object faction, 0 for neutral objects
```   

An example on how to access sonar info:
```   
for obj_type, obj_name, obj_rect, obj_team in sonar_reading:
    # Do stuff to close enemies
    if "Tank" in obj_type and obj_team!= tank_team:
        dist =  magnitude(sub(obj_rect.center, tank_pos))
        if dist < 300:
            # Do stuff
```   

Aditional functions can (and should!) be defined and used within player_input()

### Utilities
The following functions are already defined and can be used in player_input():

```   
# v = (x,y) and e = escalar, int or float
magnitude(v)                  # returns vector magnitude
normalize(v)                  # returns vector normalized (original is not replaced)
add(u, v)                     # Adds two vectors
sub(u, v)                     # Substracts u from v
dot(u, v)                     # Vectorial product
mult(v, e)                    # Multiply vector v by an escalar e

raycast(ini, dir, object_rects, max_dist, first_only=False)
                              # Gives the objects found in a line starting in ini with direction dir, until max_dist. No new objects are detected, only checks if any known object rect (passed by the user in object_rects) is in the line specified.
```
An example on how to use raycast:
```
# target_rect is the detected enemy we want shot
hit = raycast(tank_pos, gun_dir, obstacles, dist_to_enemy, first_only=True)
    if hit:
        if hit[0].center == target_rect.center:
            print("Shot is clear!")
```
### Notes on safety
The player files are run as normal python, everything is allowed, imports, calling foreign code, closing python, etc.

Do what you want, we are all consenting adults, but the game works best if you don't break it :)

## Have fun!

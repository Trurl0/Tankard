# import math

WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
YELLOW=(255,255,0)
GRAY=(150,150,150)

    
# Vector math
def magnitude(v):
    return ( sum( [i**2 for i in v] ) ) ** 0.5
    
    
def normalize(v):
    vmag = magnitude(v)
    try:
        return tuple([ v[i]/vmag  for i in range(len(v)) ])
    except Exception as e:
        return (0, 0)
        
        
def add_vector(u, v):
    return tuple([ u[i]+v[i] for i in range(len(u)) ])


def sub_vector(u, v):
    return tuple([ u[i]-v[i] for i in range(len(u)) ])


def dot_vector(u, v):
    return sum(u[i]*v[i] for i in range(len(u)))


def mult_vector(v, x):
    return tuple([i*x for i in v])


def raycast(ini, dir, obstacle_rects, max_dist, first_only=False):
    """Returns all objects found in a line from ini to dir"""
    
    hits = []
    step = 1
    point = ini
    
    for i in (x * step for x in range(0, int(max_dist*(1/step)))):
        point = add_vector(point, mult_vector(normalize(dir), step))
        for r in obstacle_rects:
            try:
                if r.collidepoint(point):
                    if r not in hits:
                        hits.append((r))
            except Exception as e:
                print(e)
        if first_only and hits:
            break       
    
    return hits
    
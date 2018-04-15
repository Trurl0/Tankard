import math

WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)
YELLOW=(255,255,0)
BLUE=(0,0,255)
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
        
        
def add(u, v):
    return [ u[i]+v[i] for i in range(len(u)) ]


def sub(u, v):
    return [ u[i]-v[i] for i in range(len(u)) ]


def dot(u, v):
    return sum(u[i]*v[i] for i in range(len(u)))


def mult(v, x):
    return tuple([i*x for i in v])


def raycast(ini, dir, objects, max_dist, first_only = False, ignore = None):
    """Returns all objects found in a line from ini to dir"""
    
    hits = []
    step = 0.1
    point = ini
    
    for i in (x * step for x in range(0, int(max_dist*(1/step)))):
        point = add(point, mult(normalize(dir), step))
        for t in objects:
            try:
                if t.rect.collidepoint(point):
                    if t is not ignore:
                        # if t not in [obj[0] for obj in hits]:
                            # hits.append((t, point))
                        if t not in hits:
                            hits.append((t))
            except Exception as e:
                print(e)
        if first_only and hits:
            break       
    
    return hits
    
    

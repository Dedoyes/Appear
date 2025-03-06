BLACK = (0, 0, 0)
ALPHABLACK = (0, 0, 0, 255)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
ALPHAWHITE = (255, 255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def max (a, b) : 
    if a > b :
        return a
    else : 
        return b 

def min (a, b) :
    if a < b : 
        return a
    else :
        return b

def F (p0, p1, p) : 
    k = (p1.y - p0.y) / (p1.x - p0.x) 
    return p.y - k * (p.x - p0.x) - p0.y  

def abs (x) :
    if x < 0 : 
        return -x
    else : 
        return x

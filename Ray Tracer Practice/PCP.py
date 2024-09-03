import numpy as np

cW, cH = 500, 500
vW, vH = 1, 1

O = (0,0,0)
d = 1

def CanvasToViewport (x,y):
    return (x*vW/cW, y*vH/cH, d)

def TraceRay(O, D, d, myInf):
    return (255,0,0) 

for x in range(-cW/2,cW/2):
    for y in range(-cH//2, cH//2):
        D = CanvasToViewport(x,y)
        color = TraceRay(O, D, 1, np.inf)
        print(color)
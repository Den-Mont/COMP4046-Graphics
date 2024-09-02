import math
from graphics import *

def polar_to_cartesian(center_x, center_y, angle, radius):
    x = center_x + radius * math.cos(math.radians(angle))
    y = center_y - radius * math.sin(math.radians(angle))
    return Point(x, y)

def angle_to_color(angle):
    r = int(127.5 * (1 + math.cos(math.radians(angle))))
    g = int(127.5 * (1 + math.cos(math.radians(angle - 120))))
    b = int(127.5 * (1 + math.cos(math.radians(angle + 120))))
    return r, g, b
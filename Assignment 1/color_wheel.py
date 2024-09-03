from graphics import *
from utils import *

def draw_color_wheel(canvas, center_x, center_y, radius_outer, radius_inner):
    for angle in range(360):
        r, g, b = angle_to_color(angle)
        color = color_rgb(r, g, b)
        
        point1_outer = polar_to_cartesian(center_x, center_y, angle, radius_outer)
        point2_outer = polar_to_cartesian(center_x, center_y, angle + 1, radius_outer)
        point1_inner = polar_to_cartesian(center_x, center_y, angle, radius_inner)
        point2_inner = polar_to_cartesian(center_x, center_y, angle + 1, radius_inner)
        
        wedge = Polygon(point1_outer, point2_outer, point2_inner, point1_inner)
        wedge.setFill(color)
        wedge.setOutline(color)
        wedge.draw(canvas)

def select_color(x, y, center_x, center_y, color_display, rgb_text):
    dx = x - center_x
    dy = y - center_y
    angle = math.degrees(math.atan2(-dy, dx)) % 360
    r, g, b = angle_to_color(angle)
    color = color_rgb(r, g, b)
    
    color_display.setFill(color)
    rgb_text.setText(f"({r},{g},{b})")
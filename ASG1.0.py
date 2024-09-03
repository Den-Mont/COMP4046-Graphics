from graphics import *
from button import *
from utils import *
from color_wheel import *
import math

# Constants
Cw, Ch = 500, 500
radius_outer = 150
radius_inner = 75

# Create the canvas
canvas = GraphWin("ASG1", Cw, Ch, autoflush=False)
canvas.setBackground("white")

# Coordinates for the center of the circle (making space for RGB values)
center_x, center_y = Cw // 2, Ch // 2

# Draw the color wheel
draw_color_wheel(canvas, center_x, center_y, radius_outer, radius_inner)

# Create elements for displaying selected color
color_display = Rectangle(Point(center_x - 50, center_y - 15), Point(center_x + 50, center_y + 15))
color_display.draw(canvas)

rgb_text = Text(Point(center_x, center_y + 30), "")
rgb_text.draw(canvas)

# Create the Quit button
quit_button = Button(canvas, Point(center_x, Ch - 25), 60, 30, "Exit")
quit_button.activate()

# Main event loop
while True:
    click_point = canvas.getMouse()
    
    if quit_button.clicked(click_point):
        break
    
    # Check if click is within the color wheel
    dx = click_point.getX() - center_x
    dy = click_point.getY() - center_y
    distance = math.sqrt(dx**2 + dy**2)
    
    if radius_inner <= distance <= radius_outer:
        select_color(click_point.getX(), click_point.getY(), center_x, center_y, color_display, rgb_text)

canvas.close()
from graphics import *
from button import *
from color_mixer import *

# Constants
Cw, Ch = 500, 400  # Increase height to accommodate K

# Create the canvas
canvas = GraphWin("ASG1.2", Cw, Ch, autoflush=False)
canvas.setBackground("white")

# Input labels
Text(Point(100, 50), "Color A:").draw(canvas)
Text(Point(100, 150), "Color B:").draw(canvas)
Text(Point(100, 300), "Result:").draw(canvas)

# RGB Labels
Text(Point(180, 30), "R").draw(canvas)
Text(Point(230, 30), "G").draw(canvas)
Text(Point(280, 30), "B").draw(canvas)
Text(Point(330, 30), "K").draw(canvas)
Text(Point(180, 130), "R").draw(canvas)
Text(Point(230, 130), "G").draw(canvas)
Text(Point(280, 130), "B").draw(canvas)
Text(Point(330, 130), "K").draw(canvas)
Text(Point(180, 280), "R").draw(canvas)
Text(Point(230, 280), "G").draw(canvas)
Text(Point(280, 280), "B").draw(canvas)
Text(Point(330, 280), "K").draw(canvas)

# RGBK Input fields for Color 1
r1_input = Entry(Point(180, 50), 3)
g1_input = Entry(Point(230, 50), 3)
b1_input = Entry(Point(280, 50), 3)
k1_input = Entry(Point(330, 50), 3)
r1_input.draw(canvas)
g1_input.draw(canvas)
b1_input.draw(canvas)
k1_input.draw(canvas)

# RGBK Input fields for Color 2
r2_input = Entry(Point(180, 150), 3)
g2_input = Entry(Point(230, 150), 3)
b2_input = Entry(Point(280, 150), 3)
k2_input = Entry(Point(330, 150), 3)
r2_input.draw(canvas)
g2_input.draw(canvas)
b2_input.draw(canvas)
k2_input.draw(canvas)

# Result fields
r_result = Entry(Point(180, 300), 3)
g_result = Entry(Point(230, 300), 3)
b_result = Entry(Point(280, 300), 3)
k_result = Entry(Point(330, 300), 3)
r_result.draw(canvas)
g_result.draw(canvas)
b_result.draw(canvas)
k_result.draw(canvas)

# Color display rectangles
color1_display = Rectangle(Point(370, 40), Point(450, 60))
color2_display = Rectangle(Point(370, 140), Point(450, 160))
result_display = Rectangle(Point(370, 290), Point(450, 310))
color1_display.draw(canvas)
color2_display.draw(canvas)
result_display.draw(canvas)

# Quit button
quit_button = Button(canvas, Point(Cw//2, Ch - 50), 60, 30, "Exit")
quit_button.activate()

# Main event loop
while True:
    click_point = canvas.checkMouse()
    
    if click_point:
        if quit_button.clicked(click_point):
            break
    
    # Mix colors whenever input changes
    mix_colors(r1_input, g1_input, b1_input, k1_input, r2_input, g2_input, b2_input, k2_input, r_result, g_result, b_result, k_result, color1_display, color2_display, result_display)

canvas.close()
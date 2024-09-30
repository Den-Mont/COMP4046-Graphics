import numpy as np
import math
from PIL import Image

# Scene configuration
cW, cH = 500, 500  # Canvas width and height
vW, vH = 1, 1  # Viewport width and height
O = np.array([0, 0, 0])  # Origin of the camera
d = 1  # Distance to projection plane

# Sphere class
class Sphere:
    def __init__(self, center, radius, color):
        self.center = np.array(center)
        self.radius = radius
        self.color = color

# Scene with spheres
scene = [
    Sphere((0, -1, 3), 1, (255, 0, 0)),  # Red
    Sphere((2, 0, 4), 1, (0, 0, 255)),  # Blue
    Sphere((-2, 0, 4), 1, (0, 255, 0))  # Green
]

BACKGROUND_COLOR = (255, 255, 255) # White Background

# Convert canvas coordinates to viewport
def CanvasToViewport(x, y):
    return np.array([x * vW / cW, y * vH / cH, d])

# Trace a ray and return the color of the closest sphere
def TraceRay(O, D, t_min, t_max):
    closest_t = float('inf')
    closest_sphere = None

    for sphere in scene:
        t1, t2 = IntersectRaySphere(O, D, sphere)

        if t_min < t1 < t_max and t1 < closest_t:
            closest_t = t1
            closest_sphere = sphere

        if t_min < t2 < t_max and t2 < closest_t:
            closest_t = t2
            closest_sphere = sphere

    if closest_sphere is None:
        return BACKGROUND_COLOR
    return closest_sphere.color

# Calculate the intersection of a ray and a sphere
def IntersectRaySphere(O, D, sphere):
    r = sphere.radius
    CO = O - sphere.center

    a = np.dot(D, D)
    b = 2 * np.dot(CO, D)
    c = np.dot(CO, CO) - r * r

    discriminant = b * b - 4 * a * c
    if discriminant < 0:
        return float('inf'), float('inf')

    t1 = (-b + math.sqrt(discriminant)) / (2 * a)
    t2 = (-b - math.sqrt(discriminant)) / (2 * a)

    return t1, t2

# Simulate ray tracing on the canvas
def Render():
    canvas = np.zeros((cH, cW, 3), dtype=np.uint8)  # Blank canvas

    for x in range(-cW // 2, cW // 2):
        for y in range(-cH // 2, cH // 2):
            # Convert canvas pixel to viewport direction 
            D = CanvasToViewport(x, y)
            color = TraceRay(O, D, 1, float('inf'))
            # Correct the canvas indexing (flip y-axis)
            canvas[cH // 2 - y - 1, x + cW // 2] = color

    return canvas

# Render the scene and save the result
image_data = Render()

# Convert to an Image and save as PNG
image = Image.fromarray(image_data)
image.save("ray_traced_scene.png")
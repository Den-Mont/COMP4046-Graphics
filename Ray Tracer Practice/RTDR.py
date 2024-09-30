import numpy as np
import math
from PIL import Image

# Simple Ray Tracing with Diffuse Reflection

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
        self.color = np.array(color)

# Light class
class Light:
    def __init__(self, light_type, intensity, position=None, direction=None):
        self.light_type = light_type
        self.intensity = intensity
        self.position = np.array(position) if position else None
        self.direction = np.array(direction) if direction else None

# Scene with spheres and lights
scene = [
    Sphere((0, -1, 3), 1, (255, 0, 0)),  # Red
    Sphere((2, 0, 4), 1, (0, 0, 255)),  # Blue
    Sphere((-2, 0, 4), 1, (0, 255, 0)),  # Green
    Sphere((0, -5001, 0), 5000, (255, 255, 0))  # Yellow ground
]

lights = [
    Light('ambient', 0.2),
    Light('point', 0.6, position=(2, 1, 0)),
    Light('directional', 0.2, direction=(1, 4, 4))
]

BACKGROUND_COLOR = (255, 255, 255)  # White Background

# Convert canvas coordinates to viewport
def CanvasToViewport(x, y):
    return np.array([x * vW / cW, y * vH / cH, d])

# Calculate lighting at a point
def ComputeLighting(P, N):
    intensity = 0.0
    for light in lights:
        if light.light_type == 'ambient':
            intensity += light.intensity
        else:
            if light.light_type == 'point':
                L = light.position - P
            else:
                L = light.direction

            n_dot_l = np.dot(N, L)
            if n_dot_l > 0:
                intensity += light.intensity * n_dot_l / (np.linalg.norm(N) * np.linalg.norm(L))
    
    return intensity

# Trace a ray and return the color of the closest sphere with lighting
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
    
    # Compute intersection point and normal
    P = O + closest_t * D
    N = P - closest_sphere.center
    N = N / np.linalg.norm(N)  # Normalize the normal

    # Compute lighting at the intersection point
    lighting_intensity = ComputeLighting(P, N)

    # Adjust the color based on lighting
    return np.clip(closest_sphere.color * lighting_intensity, 0, 255)

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
image = Image.fromarray(image_data.astype('uint8'))
image.save("ray_traced_scene_with_lighting.png")

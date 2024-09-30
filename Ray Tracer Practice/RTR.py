import numpy as np
import math
from graphics import *

# Simple Ray Tracing with Diffuse, Specular Reflection, Shadows, and Reflections

# Scene configuration
cW, cH = 500, 500  # Canvas width and height
vW, vH = 1, 1  # Viewport width and height
O = np.array([0, 0, 0])  # Origin of the camera
d = 1  # Distance to projection plane
MAX_RECURSION_DEPTH = 3  # Maximum recursion depth for reflections

# Sphere class with reflectivity
class Sphere:
    def __init__(self, center, radius, color, specular, reflective):
        self.center = np.array(center)
        self.radius = radius
        self.color = np.array(color)
        self.specular = specular
        self.reflective = reflective

# Light class
class Light:
    def __init__(self, light_type, intensity, position=None, direction=None):
        self.light_type = light_type
        self.intensity = intensity
        self.position = np.array(position) if position else None
        self.direction = np.array(direction) if direction else None

# Scene with spheres and lights
scene = [
    Sphere((0, -1, 3), 1, (255, 0, 0), 500, 0.2),  # Red, slightly reflective
    Sphere((2, 0, 4), 1, (0, 0, 255), 500, 0.3),  # Blue, more reflective
    Sphere((-2, 0, 4), 1, (0, 255, 0), 10, 0.4),  # Green, even more reflective
    Sphere((0, -5001, 0), 5000, (255, 255, 0), 1000, 0.5)  # Yellow ground, half reflective
]

lights = [
    Light('ambient', 0.2),
    Light('point', 0.6, position=(2, 1, 0)),
    Light('directional', 0.2, direction=(1, 4, 4))
]

BACKGROUND_COLOR = (0, 0, 0)  # Black Background

# Convert canvas coordinates to viewport
def CanvasToViewport(x, y):
    return np.array([x * vW / cW, y * vH / cH, d])

# Calculate the closest intersection with any sphere in the scene
def ClosestIntersection(O, D, t_min, t_max):
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
    return closest_sphere, closest_t

# Calculate lighting at a point, including diffuse, specular reflections, and shadows
def ComputeLighting(P, N, V, s):
    intensity = 0.0
    for light in lights:
        if light.light_type == 'ambient':
            intensity += light.intensity
        else:
            if light.light_type == 'point':
                L = light.position - P
                t_max = 1
            else:
                L = light.direction
                t_max = float('inf')

            # Shadow check
            shadow_sphere, shadow_t = ClosestIntersection(P, L, 0.001, t_max)
            if shadow_sphere is not None:
                continue  # There's a shadow, skip this light

            # Diffuse reflection
            n_dot_l = np.dot(N, L)
            if n_dot_l > 0:
                intensity += light.intensity * n_dot_l / (np.linalg.norm(N) * np.linalg.norm(L))

            # Specular reflection
            if s != -1:
                R = 2 * N * np.dot(N, L) - L
                r_dot_v = np.dot(R, V)
                if r_dot_v > 0:
                    intensity += light.intensity * (r_dot_v / (np.linalg.norm(R) * np.linalg.norm(V))) ** s

    return intensity

# Reflect a ray around a normal
def ReflectRay(R, N):
    return 2 * N * np.dot(N, R) - R

# Trace a ray and return the color of the closest sphere with lighting, shadows, specular reflection, and reflections

def TraceRay(O, D, t_min, t_max, recursion_depth):
    closest_sphere, closest_t = ClosestIntersection(O, D, t_min, t_max)
    if closest_sphere is None:
        return BACKGROUND_COLOR

    # Compute intersection point and normal
    P = O + closest_t * D
    N = P - closest_sphere.center
    N = N / np.linalg.norm(N)  # Normalize the normal

    # Compute the view direction
    V = -D  # The view direction is the inverse of the ray direction

    # Compute local color based on lighting
    local_color = closest_sphere.color * ComputeLighting(P, N, V, closest_sphere.specular)

    # Check for reflection
    r = closest_sphere.reflective
    if recursion_depth <= 0 or r <= 0:
        return local_color

    # Compute the reflected color recursively
    R = ReflectRay(-D, N)
    reflected_color = TraceRay(P, R, 0.001, float('inf'), recursion_depth - 1)

    # Combine local color and reflected color based on reflectivity
    return np.clip(np.array(local_color) * (1 - r) + np.array(reflected_color) * r, 0, 255)

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
    win = GraphWin("Reflection", 500, 500, autoflush=False)  # Initialize window with autoflush=False
    win.setBackground(color_rgb(*BACKGROUND_COLOR))  # Set the background color

    for x in range(-cW // 2, cW // 2):
        for y in range(-cH // 2, cH // 2):
            # Convert canvas pixel to viewport direction 
            D = CanvasToViewport(x, y)
            color = TraceRay(O, D, 1, float('inf'), MAX_RECURSION_DEPTH)
            # Draw the pixel
            win.plotPixel(cW // 2 + x, cH // 2 - y, color_rgb(int(color[0]), int(color[1]), int(color[2])))

        # Update the window at the end of each row to create an animation effect
        win.update()

    win.getMouse()  # Wait for mouse click to close the window
    win.close()

# Render the scene
Render()

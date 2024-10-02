import numpy as np
import math
from graphics import *

# Scene configuration
cW, cH = 500, 500  # Canvas width and height
vW, vH = 1, 1  # Viewport width and height
d = 1  # Distance to projection plane

BACKGROUND_COLOR = (0, 0, 0)  # Black Background

# Camera class
class Camera:
    def __init__(self, position, look_at):
        self.position = np.array(position)
        self.rotation_matrix = self.LookAt(look_at)

    # LookAt function to generate a rotation matrix for the camera
    def LookAt(self, target):
        forward = target - self.position
        forward = forward / np.linalg.norm(forward)

        # Assuming "up" direction is Y-axis, we'll generate a basis for the camera's orientation
        right = np.cross(np.array([0, 1, 0]), forward)
        right = right / np.linalg.norm(right)

        up = np.cross(forward, right)

        # Rotation matrix using the right, up, and forward vectors as the camera basis
        rotation_matrix = np.array([right, up, forward])
        return rotation_matrix.T  # Transpose to use as transformation matrix

# Sphere class
class Sphere:
    def __init__(self, center, radius, color, specular):
        self.center = np.array(center)
        self.radius = radius
        self.color = np.array(color)
        self.specular = specular

# Light class
class Light:
    def __init__(self, light_type, intensity, position=None, direction=None):
        self.light_type = light_type
        self.intensity = intensity
        self.position = np.array(position) if position else None
        self.direction = np.array(direction) if direction else None

# Scene with spheres and lights
scene = [
    Sphere((0, -1, 3), 1, (255, 0, 0), 500),  # Red sphere
    Sphere((2, 0, 4), 1, (0, 0, 255), 500),  # Blue sphere
    Sphere((-2, 0, 4), 1, (0, 255, 0), 10),  # Green sphere
    Sphere((0, -5001, 0), 5000, (255, 255, 0), 1000)  # Large yellow ground
]

lights = [
    Light('ambient', 0.2),
    Light('point', 0.6, position=(2, 1, 0)),
    Light('directional', 0.2, direction=(1, 4, 4))
]

# Convert canvas coordinates to viewport and apply camera rotation
def CanvasToViewport(x, y, camera):
    D = np.array([x * vW / cW, y * vH / cH, d])
    return camera.rotation_matrix @ D  # Apply camera rotation to the direction vector

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

# Trace a ray and return the color of the closest sphere with lighting, shadows, and specular reflection
def TraceRay(O, D, t_min, t_max):
    closest_sphere, closest_t = ClosestIntersection(O, D, t_min, t_max)
    if closest_sphere is None:
        return BACKGROUND_COLOR

    # Compute intersection point and normal
    P = O + closest_t * D
    N = P - closest_sphere.center
    N = N / np.linalg.norm(N)  # Normalize the normal

    # Compute the view direction
    V = -D  # The view direction is the inverse of the ray direction

    # Compute lighting at the intersection point
    lighting_intensity = ComputeLighting(P, N, V, closest_sphere.specular)

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
def Render(camera):
    win = GraphWin("Ray Tracing", 500, 500, autoflush=False)  # Initialize window
    win.setBackground(color_rgb(*BACKGROUND_COLOR))  # Set the background to black

    for x in range(-cW // 2, cW // 2):
        for y in range(-cH // 2, cH // 2):
            # Convert canvas pixel to viewport direction and apply camera rotation
            D = CanvasToViewport(x, y, camera)
            color = TraceRay(camera.position, D, 1, float('inf'))
            # Draw the pixel
            win.plotPixel(cW // 2 + x, cH // 2 - y, color_rgb(int(color[0]), int(color[1]), int(color[2])))

        # Update the window at the end of each row to create an animation effect
        win.update()

    win.getMouse()  # Wait for mouse click to close the window
    win.close()

# Create a camera with a specific position and rotation matrix
camera = Camera(
    position=[3, 0.6, -3],  # Camera position 
    look_at=[1.2, -1, 3]  # Looking at (0,0,3 for the center of the scene)
)

# Render the scene
Render(camera)

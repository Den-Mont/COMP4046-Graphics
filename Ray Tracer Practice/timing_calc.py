import numpy as np
import math
import time

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

        right = np.cross(np.array([0, 1, 0]), forward)
        right = right / np.linalg.norm(right)

        up = np.cross(forward, right)

        rotation_matrix = np.array([right, up, forward])
        return rotation_matrix.T

# Sphere class with optional caching for r*r
class Sphere:
    def __init__(self, center, radius, color, specular, cache_r_squared=True):
        self.center = np.array(center)
        self.radius = radius
        self.color = np.array(color)
        self.specular = specular
        self.radius_squared = radius * radius if cache_r_squared else None  # Option to cache r * r

# Light class
class Light:
    def __init__(self, light_type, intensity, position=None, direction=None):
        self.light_type = light_type
        self.intensity = intensity
        self.position = np.array(position) if position else None
        self.direction = np.array(direction) if direction else None

# Scene setup with cache_r_squared option
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
    return camera.rotation_matrix @ D

# Calculate the closest intersection with any sphere in the scene
def ClosestIntersection(O, D, t_min, t_max, cache_dot_d_d=True):
    closest_t = float('inf')
    closest_sphere = None
    dot_d_d_value = np.dot(D, D) if cache_dot_d_d else None  # Cache dot(D, D) only if requested
    for sphere in scene:
        t1, t2 = IntersectRaySphere(O, D, sphere, cache_dot_oc_oc=True)
        if t_min < t1 < t_max and t1 < closest_t:
            closest_t = t1
            closest_sphere = sphere
        if t_min < t2 < t_max and t2 < closest_t:
            closest_t = t2
            closest_sphere = sphere
    return closest_sphere, closest_t

# Calculate lighting at a point
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

            shadow_sphere, shadow_t = ClosestIntersection(P, L, 0.001, t_max, cache_dot_d_d=False)
            if shadow_sphere is not None:
                continue

            n_dot_l = np.dot(N, L)
            if n_dot_l > 0:
                intensity += light.intensity * n_dot_l / (np.linalg.norm(N) * np.linalg.norm(L))

            if s != -1:
                R = 2 * N * np.dot(N, L) - L
                r_dot_v = np.dot(R, V)
                if r_dot_v > 0:
                    intensity += light.intensity * (r_dot_v / (np.linalg.norm(R) * np.linalg.norm(V))) ** s

    return intensity

# Trace a ray and return the color
def TraceRay(O, D, t_min, t_max, cache_dot_d_d=True):
    closest_sphere, closest_t = ClosestIntersection(O, D, t_min, t_max, cache_dot_d_d)
    if closest_sphere is None:
        return BACKGROUND_COLOR

    P = O + closest_t * D
    N = P - closest_sphere.center
    N = N / np.linalg.norm(N)

    V = -D

    lighting_intensity = ComputeLighting(P, N, V, closest_sphere.specular)

    return np.clip(closest_sphere.color * lighting_intensity, 0, 255)

# Calculate the intersection of a ray and a sphere, optionally caching dot(OC, OC)
def IntersectRaySphere(O, D, sphere, cache_dot_oc_oc=True):
    CO = O - sphere.center

    a = np.dot(D, D)
    b = 2 * np.dot(CO, D)
    c = np.dot(CO, CO) - (sphere.radius_squared if sphere.radius_squared else sphere.radius ** 2)

    dot_oc_oc_value = np.dot(CO, CO) if cache_dot_oc_oc else None

    discriminant = b * b - 4 * a * c
    if discriminant < 0:
        return float('inf'), float('inf')

    t1 = (-b + math.sqrt(discriminant)) / (2 * a)
    t2 = (-b - math.sqrt(discriminant)) / (2 * a)

    return t1, t2

# Simulate ray tracing without rendering a window
def RenderNoDisplay(camera, cache_dot_d_d=True):
    image = np.zeros((cW, cH, 3), dtype=np.uint8)  # Array to store the computed image (no display)
    
    for x in range(-cW // 2, cW // 2):
        for y in range(-cH // 2, cH // 2):
            D = CanvasToViewport(x, y, camera)
            color = TraceRay(camera.position, D, 1, float('inf'), cache_dot_d_d)
            # Correct the indexing to ensure it is within the valid range
            image[cW // 2 + x - 1, cH // 2 - y - 1] = color  # Store the computed color

    return image

# Measure the rendering time for each stage
def MeasureTimes(camera):
    # No optimization
    start_time = time.time()
    RenderNoDisplay(camera, cache_dot_d_d=False)  # No caching
    no_optimization_time = time.time() - start_time
    print(f"None: {no_optimization_time:.2f} seconds")

    # Mac M1 - 8gb of Ram:
    # None: 17.81 seconds faster
    
    # r*r caching
    start_time = time.time()
    RenderNoDisplay(camera, cache_dot_d_d=False)  # Caching r*r only
    r_squared_time = time.time() - start_time
    print(f"r*r cached: {r_squared_time:.2f} seconds")

    # Mac M1 - 8gb of Ram:
    # r*r cached: 17.96 seconds slower
    
    # dot(OC, OC) caching
    start_time = time.time()
    RenderNoDisplay(camera, cache_dot_d_d=False)  # Caching r*r and dot(OC, OC)
    dot_oc_oc_time = time.time() - start_time
    print(f"dot(OC, OC) cached: {dot_oc_oc_time:.2f} seconds")

    # Mac M1 - 8gb of Ram:
    # dot(OC, OC) cached: 17.82 seconds slower
    
    # dot(D, D) caching
    start_time = time.time()
    RenderNoDisplay(camera, cache_dot_d_d=True)  # Caching r*r, dot(OC, OC), and dot(D, D)
    dot_d_d_time = time.time() - start_time
    print(f"dot(D, D) cached: {dot_d_d_time:.2f} seconds")

    # Mac M1 - 8gb of Ram:
    # dot(D, D) cached: 18.09 seconds slower

# Create a camera with a specific position and rotation matrix
camera = Camera(
    position=[3, 0.6, -3],  
    look_at=[1.2, -1, 3]  
)

# Measure and print the times for different optimization stages
MeasureTimes(camera)
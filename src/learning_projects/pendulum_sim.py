import pygame
import math
import sys
import random
from src.vector_operations import *

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pendulum Simulation")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Global parameters
gravity = 1
damping = 1.1
max_length = 10000
dragging = False
simulation_started = False

class Pendulum:
    def __init__(self, origin, length, angle=math.pi, num_pendulums=1, length_multiplier=1, auto_start=False):
        self.origin = origin
        self.length = length
        self.angle = angle
        self.angular_velocity = 0
        self.angular_acceleration = 0
        self.path = []  # List to store the path points
        self.child_pendulums = []  # List to store child pendulums
        self.auto_start = auto_start

        if self.auto_start:
            global simulation_started
            simulation_started = True

        # Create child pendulums recursively
        if num_pendulums > 1:
            child_length = length * length_multiplier  # Adjust this factor to control the length of child pendulums
            child_origin = Vector(self.origin['x'] + self.length * math.sin(self.angle),
                                  self.origin['y'] + self.length * math.cos(self.angle))  # Place child beneath parent
            self.child_pendulums.append(Pendulum(child_origin, child_length, angle, num_pendulums - 1, length_multiplier, auto_start))

    def update(self):
        global gravity, damping, dragging, simulation_started
        if simulation_started and not dragging:
            self.angular_acceleration = (-gravity / self.length) * math.sin(self.angle)
            self.angular_velocity += self.angular_acceleration
            self.angular_velocity *= damping
            self.angle += self.angular_velocity

        # Calculate the current end point of the pendulum
        endpoint = Vector(self.origin['x'] + self.length * math.sin(self.angle),
                          self.origin['y'] + self.length * math.cos(self.angle))

        # Append the current end point to the path
        if simulation_started and not dragging:
            self.path.append(endpoint)

        # Limit the length of the path to prevent memory overflow
        if len(self.path) > max_length:  # Adjust this value as needed
            self.path.pop(0)

        # Update child pendulums if they exist
        for child_pendulum in self.child_pendulums:
            child_pendulum.origin = endpoint  # Set child's origin to the current endpoint of the parent
            child_pendulum.update()  # Update the child pendulum

    def draw(self, screen):
        # Draw the pendulum path for the parent only
        if len(self.path) > 1 and len(self.child_pendulums) == 0:
            pygame.draw.lines(screen, (0,100,255), False, [vecToTuple(point) for point in self.path], 2)

        # Draw the pendulum
        endpoint = Vector(self.origin['x'] + self.length * math.sin(self.angle),
                          self.origin['y'] + self.length * math.cos(self.angle))
        pygame.draw.line(screen, WHITE, vecToTuple(self.origin), vecToTuple(endpoint), 2)
        
        # Draw fulcrum point
        if not self.child_pendulums:
            pygame.draw.circle(screen, BLUE, vecToTuple(endpoint), 6)  # Larger blue circle for the end of the last pendulum
        else:
            pygame.draw.circle(screen, WHITE, vecToTuple(endpoint), 4)  # Smaller white circles for intermediate points

        # Draw child pendulums
        for child_pendulum in self.child_pendulums:
            child_pendulum.draw(screen)

    def get_end_point(self):
        if self.child_pendulums:
            return self.child_pendulums[0].get_end_point()
        else:
            return Vector(self.origin['x'] + self.length * math.sin(self.angle),
                          self.origin['y'] + self.length * math.cos(self.angle))

    def set_position_from_end(self, pos):
        dx = pos['x'] - self.origin['x']
        dy = pos['y'] - self.origin['y']
        distance = math.hypot(dx, dy)
        self.angle = math.atan2(dx, dy)
        self.angular_velocity = 0
        self.angular_acceleration = 0
        if self.child_pendulums:
            child_origin = Vector(self.origin['x'] + self.length * math.sin(self.angle),
                                  self.origin['y'] + self.length * math.cos(self.angle))
            self.child_pendulums[0].origin = child_origin
            self.child_pendulums[0].set_position_from_end(pos)

    def constrain_within_length(self, pos, max_length):
        dx = pos['x'] - self.origin['x']
        dy = pos['y'] - self.origin['y']
        distance = math.hypot(dx, dy)
        if distance > max_length:
            scale = max_length / distance
            dx *= scale
            dy *= scale
        return {'x': self.origin['x'] + dx, 'y': self.origin['y'] + dy}

# Main loop
running = True
clock = pygame.time.Clock()

# Create pendulum with multiple pendulums chained together
origin = Vector(WIDTH // 2, HEIGHT // 2)
total_length = 250  # Total length of the pendulum chain
num_pendulums = 10  # Number of pendulums in the chain
length_per_pendulum = total_length / num_pendulums  # Length of each pendulum
pendulum = Pendulum(origin, length_per_pendulum, math.pi, num_pendulums, 0.9, auto_start=False)  # Set auto_start to True or False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            end_pos = vecToTuple(pendulum.get_end_point())
            if math.hypot(mouse_pos[0] - end_pos[0], mouse_pos[1] - end_pos[1]) < 10:
                dragging = True
                simulation_started = True
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        elif event.type == pygame.MOUSEMOTION and dragging:
            mouse_pos = pygame.mouse.get_pos()
            constrained_pos = pendulum.constrain_within_length({'x': mouse_pos[0], 'y': mouse_pos[1]}, total_length)
            pendulum.set_position_from_end(constrained_pos)

    pendulum.update()

    screen.fill(BLACK)
    pendulum.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

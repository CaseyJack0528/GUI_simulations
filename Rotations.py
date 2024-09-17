import pygame
import random
import math
import sys
import numpy as np

##########################################################################################
#Cube properties
cube_length = 500
cube_width = 100
cube_height = 100
cube_center = 0 # [x, y, z] or 0 for cube at center of screen

#Rotation properties 
x_rotation_speed = 50 #deg/sec
y_rotation_speed = 10 #deg/sec
z_rotation_speed = 0 #deg/sec
##########################################################################################

vertex_size = 5

pygame.init()
window_size = pygame.display.Info()
screen_width = window_size.current_w
screen_height = window_size.current_h
print(pygame.display.Info())
#screen_width = 1200
#screen_height = 800

#Convert degrees to radians for python functions
x_rotation_speed *= 2*math.pi/360
y_rotation_speed *= 2*math.pi/360
z_rotation_speed *= 2*math.pi/360

#Initiate angle values
x_anglei = 0
y_anglei = 0
z_anglei = 0

if cube_center == 0:
    cube_center = [int(screen_width/2), int(screen_height/2), 0]

screen = pygame.display.set_mode((screen_width, screen_height))
running = True

##########################################################################################
class circle:

    def __init__(self, radius, color, x, y, z):
        self.radius = radius
        self.color = color
        self.x = x
        self.y = y
        self.z = z

    def draw_circle(self):
        pygame.draw.circle(screen, self.color, (int(self.x + cube_center[0]), int(self.y + cube_center[1])), self.radius)


    def update_position(self):
        position_array = np.array([self.x, self.y, self.z])
        rotation_matrix = np.array(Rx)
        print(rotation_matrix)
        temp_array = np.dot(rotation_matrix, position_array)
        #print(temp_array)
        self.x = temp_array[0]#[0]
        self.y = temp_array[1]#[0]
        self.z = temp_array[2]#[0]
        

##########################################################################################
def matrix_dot_product(matrix_1, matrix_2):
    pass


def create_cube(length, width, height):
    global cube_vertices
    length = int(length/2)
    width = int(width/2)
    height = int(height/2)
    #For each vertex [x, y, z]
    #Start at top back left, clockwise; then bottom back left, clockwise
    cube_vertices[0] = [-width, height, -length]
    cube_vertices[1] = [width, height, -length]
    cube_vertices[2] = [width, height, length]
    cube_vertices[3] = [-width, height, length]
    cube_vertices[4] = [-width, -height, -length]
    cube_vertices[5] = [width, -height, -length]
    cube_vertices[6] = [width, -height, length]
    cube_vertices[7] = [-width, -height, length]
    
##########################################################################################

#Rotation matrices [row][column]
Rx = [[1, 0, 0],
      [0, 0, 0],
      [0, 0, 0]]

Ry = [[0, 0, 0],
      [0, 1, 0],
      [0, 0, 0]]

Rz = [[0, 0, 0],
      [0, 0, 0],
      [0, 0, 1]]

def update_rotation_matrices(angle_x, angle_y, angle_z):
    global Rx, Ry, Rz
    # X rotation matrix
    Rx[1][1] = math.cos(angle_x)
    Rx[2][2] = math.cos(angle_x)
    Rx[1][2] = -math.sin(angle_x)
    Rx[2][1] = math.sin(angle_x)

    # Y rotation matrix
    Ry[0][0] = math.cos(angle_y)
    Ry[0][2] = math.sin(angle_y)
    Ry[2][0] = -math.sin(angle_y)
    Ry[2][2] = math.cos(angle_y)

    # Z rotation matrix
    Rz[0][0] = math.cos(angle_z)
    Rz[1][0] = math.sin(angle_z)
    Rz[0][1] = -math.sin(angle_z)
    Rz[1][1] = math.cos(angle_z)

#Update angles
def update_angles():
    global x_angle, y_angle, z_angle
    x_angle = x_anglei + x_rotation_speed*t
    y_angle = y_anglei + y_rotation_speed*t
    z_angle = z_anglei + z_rotation_speed*t
    if x_angle > (2*math.pi):
        x_angle -= (2*math.pi)
    if y_angle > (2*math.pi):
        y_angle -= (2*math.pi)
    if z_angle > (2*math.pi):
        z_angle -= (2*math.pi)

    

##########################################################################################
#Create vertices for cube
cube_vertices = [0 for i in range(8)]
create_cube(cube_length, cube_width, cube_height)

circles = [0 for i in range(8)]
for vertex in range(8):
    circles[vertex] = circle(vertex_size, (255, 0, 0), cube_vertices[vertex][0], cube_vertices[vertex][1], cube_vertices[vertex][2])
##########################################################################################

clock = pygame.time.Clock()
while running:
    screen.fill((0, 0, 0))  # Fill the background with black
    for vertex in range(8):
        circles[vertex].update_position()
        circles[vertex].draw_circle()

    #circles[0].update_position()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    t = pygame.time.get_ticks()/1000
    update_angles()
    update_rotation_matrices(x_angle, y_angle, z_angle)
    pygame.display.flip()
    if pygame.key.get_pressed()[pygame.K_v]:
        sys.exit()

pygame.quit()
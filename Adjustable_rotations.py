import pygame
import math
import sys
import numpy as np

##########################################################################################
#Cube properties
cube_length = 200
cube_width = 100
cube_height = 100
cube_center = 0 # [x, y, z] or 0 for cube at center of screen

#Rotation properties 
x_rotation_speed = 0 #deg/sec
y_rotation_speed = 0 #deg/sec
z_rotation_speed = 0 #deg/sec
##########################################################################################

vertex_size = 5
cube_color = (255, 0, 255)
scroll_sensitivity = 1.07
rotation_sensitivity = 0.005

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
        self.xi = x
        self.yi = y
        self.zi = z

    def draw_circle(self):
        pygame.draw.circle(screen, self.color, (int(self.x + cube_center[0]), int(self.y + cube_center[1])), self.radius)


    def update_position(self):
        position_array = [[self.xi], [self.yi], [self.zi]]
        temp_array = np.dot(Rx, Ry)
        temp_array = np.dot(Rz, temp_array)
        temp_array = np.dot(temp_array, position_array)
        self.x = temp_array[0][0]
        self.y = temp_array[1][0]
        self.z = temp_array[2][0]
        

##########################################################################################
def connect_the_dots(v1, v2):
    pygame.draw.line(screen, cube_color, (circles[v1].x + cube_center[0], circles[v1].y + cube_center[1]), (circles[v2].x + cube_center[0], circles[v2].y + cube_center[1]), 5)


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
    x_angle = x_angle + x_rotation_speed
    y_angle = y_angle + y_rotation_speed
    z_angle = z_angle + z_rotation_speed
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
    circles[vertex] = circle(vertex_size, cube_color, cube_vertices[vertex][0], cube_vertices[vertex][1], cube_vertices[vertex][2])
##########################################################################################

clock = pygame.time.Clock()
mouse_down = 0
x_angle = 0
y_angle = 0
z_angle = 0
while running:
    screen.fill((0, 0, 0))  # Fill the background with black
    for vertex in range(8):
        circles[vertex].update_position()
        circles[vertex].draw_circle()

    for i in range(3):
        connect_the_dots(i, i+1)
    for i in range(4, 7):
        connect_the_dots(i, i+1)
    connect_the_dots(0, 3)
    connect_the_dots(4, 7)
    connect_the_dots(0, 4)
    connect_the_dots(3, 7)
    connect_the_dots(1, 5)
    connect_the_dots(2, 6)


    #Detect user events (mouse and keyboard)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            #If left mouse button pressed
            if event.button == 1:
                mouse_down = 1
                start_position_x = pygame.mouse.get_pos()[0]
                start_position_y = pygame.mouse.get_pos()[1]
        if event.type == pygame.MOUSEBUTTONUP:
            #If left mouse button released
            if event.button == 1:
                mouse_down = 0
                for vertex in range(8):
                    circles[vertex].xi = circles[vertex].x
                    circles[vertex].yi = circles[vertex].y
                    circles[vertex].zi = circles[vertex].z
                    x_angle = 0
                    y_angle = 0
                    z_angle = 0
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                cube_height *= scroll_sensitivity*event.y
                cube_length *= scroll_sensitivity*event.y
                cube_width *= scroll_sensitivity*event.y
            if event.y < 0:
                cube_height /= -scroll_sensitivity*event.y
                cube_length /= -scroll_sensitivity*event.y
                cube_width /= -scroll_sensitivity*event.y
            if cube_height < 1:
                cube_height = 1
            if cube_length < 1:
                cube_length = 1
            if cube_width < 1:
                cube_width = 1
            create_cube(cube_length, cube_width, cube_height)
            for vertex in range(8):
                circles[vertex] = circle(vertex_size, cube_color, cube_vertices[vertex][0], cube_vertices[vertex][1], cube_vertices[vertex][2])
                circles[vertex].update_position()
                circles[vertex].draw_circle()

    if mouse_down == 1:
        y_angle = rotation_sensitivity*(pygame.mouse.get_pos()[0] - start_position_x)
        x_angle = -rotation_sensitivity*(pygame.mouse.get_pos()[1] - start_position_y)
        pygame.draw.line(screen, (255, 0, 0), (start_position_x, start_position_y), (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]), 5)

    t = pygame.time.get_ticks()/1000
    update_angles()
    update_rotation_matrices(x_angle, y_angle, z_angle)
    pygame.display.flip()
    if pygame.key.get_pressed()[pygame.K_v]:
        sys.exit()

pygame.quit()
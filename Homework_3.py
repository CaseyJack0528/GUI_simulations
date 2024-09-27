import pygame
import random
import math
import sys
import numpy as np
import time

##########################################################################################
arm_width = 5
# Fill in DH table with theta, alpha, d, and a (in that order) for each row
DH_table = [[0, -90, 1, 0],
            [90, 0, 0, 0],
            [0, -90, 1, 0],
            [0, 180, 1, 0],
            [0, -90, 0, 0],
            [0, 90, 0, 0],
            [0, 0, 1, 0]]
##########################################################################################

scale = 100
offset_x = 0
offset_y = 0

def convert_to_radians():
    for i in range(len(DH_table)):
        DH_table[i][0] *= 2*math.pi/360
        DH_table[i][1] *= 2*math.pi/360
        DH_table[i][2] *= scale
        DH_table[i][3] *= scale

pygame.init()
window_size = pygame.display.Info()
screen_width = window_size.current_w
screen_height = window_size.current_h
print(pygame.display.Info())
#screen_width = 1200
#screen_height = 800

starting_position = [0, 0, 0, 1]

screen = pygame.display.set_mode((screen_width, screen_height))
running = True


    
##########################################################################################

#Rotation matrix [row][column]
transformation_matrix = [[0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 1]]


def update_transformation_matrix(theta, alpha, d, a):
    global transformation_matrix
    # DH transformation matrix formula
    # Row 1
    transformation_matrix[0][0] = math.cos(theta)
    transformation_matrix[0][1] = -math.sin(theta)*math.cos(alpha)
    transformation_matrix[0][2] = math.sin(theta)*math.sin(alpha)
    transformation_matrix[0][3] = a*math.cos(theta)
    # Row 2
    transformation_matrix[1][0] = math.sin(theta)
    transformation_matrix[1][1] = math.cos(theta)*math.cos(alpha)
    transformation_matrix[1][2] = -math.cos(theta)*math.sin(alpha)
    transformation_matrix[1][3] = a*math.sin(theta)
    # Row 3
    transformation_matrix[2][1] = math.sin(alpha)
    transformation_matrix[2][2] = math.cos(alpha)
    transformation_matrix[2][3] = d

##########################################################################################

def update_link(position):
    position_array = [[position[0]],
                      [position[1]],
                      [position[2]],
                      [position[3]]]
    temp_array = np.dot(transformation_matrix, position_array)
    position = [temp_array[0][0], temp_array[1][0], temp_array[2][0], 1]
    return position

##########################################################################################

def draw_link(starting, ending):
    #starting[0] += offset_x
    #starting[1] += offset_y
    #ending[0] += offset_x
    #ending[1] += offset_y
    starting = correct_display(starting)
    #ending = correct_display(ending)
    pygame.draw.line(screen, [0, 255, 0], (int(starting[0]), int(starting[1])), (int(ending[0]), int(ending[1])), arm_width)

##########################################################################################

def correct_display(point):
    print(point)
    point[1] = screen_height-point[1]
    print(point)
    return point

##########################################################################################
clock = pygame.time.Clock()

mouse_down = 0
convert_to_radians()
LMB_down = 0
while running:
    starting_position = [0, 0, 0, 1]
    clock.tick(60)
    screen.fill((0, 0, 0))  # Fill the background with black
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #If mouse button pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                LMB_down = 1
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                LMB_down = 0
    #pygame.draw.circle(screen, [255, 0, 0], (int(starting_position[0]), int(starting_position[1])), 10)
    if LMB_down == 1:
        offset_x = pygame.mouse.get_pos()[0]
        offset_y = pygame.mouse.get_pos()[1]
    for link in range(len(DH_table)):
        update_transformation_matrix(DH_table[link][0], DH_table[link][1], DH_table[link][2], DH_table[link][3])
        draw_link(starting_position, update_link(starting_position))
        starting_position = update_link(starting_position)
    #t = pygame.time.get_ticks()/1000
    pygame.display.flip()
    #time.sleep(0.1)
    if pygame.key.get_pressed()[pygame.K_v]:
        sys.exit()

pygame.quit()
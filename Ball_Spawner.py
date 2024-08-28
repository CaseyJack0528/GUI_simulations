import pygame
import random
import math
import time
import sys

#######################################################################################
#Adjustable parameters
number_of_circles = 1 #Number of circles to spawn
random_position = 0 #Start in a random position? (1=yes, 0=no)
#######################################################################################


pygame.init()
window_size = pygame.display.Info()
screen_width = window_size.current_w
screen_height = window_size.current_h
print(pygame.display.Info())
#screen_width = 1200
#screen_height = 800

skipx = 0
skipy = 0

screen = pygame.display.set_mode((screen_width, screen_height))
running = True


def initial_conditions(radius):
    if random_position == 1:
        #Random starting positions
        x = random.randint(radius, (screen_width - radius))
        y = random.randint(radius, (screen_height - radius))
    else:
        x = screen_width/2
        y = screen_height/2
    #Random starting velocity 
    direction_start = random.randint(0, 360)
    dx = 500*math.cos(direction_start)
    dy = 500*math.sin(direction_start)
    #Starting acceleration
    acceleration_x = 0 #random.randint(50, 100)
    acceleration_y = 0 #random.randint(50, 100)
    #Random color
    R = random.randint(0, 255)
    G = random.randint(0, 255)
    B = random.randint(0, 255)
    RGB = (R, G, B)
    return x, y, dx, dy, acceleration_x, acceleration_y, RGB

class circle:

    def __init__(self, radius, x, y, dx, dy, acceleration_x, acceleration_y, RGB):
        self.radius = radius
        self.x = x
        self.y = y
        self.dx = dx
        self.dy =dy
        self.acceleration_x = acceleration_x
        self.acceleration_y = acceleration_y
        self.RGB = RGB

    radius = 25

    def update_velocities(self):
        self.dx = self.dx + self.acceleration_x*t
        self.dy = self.dy + self.acceleration_y*t

    def update_positions(self):
        global skipx
        global skipy

        #Update X
        if (self.x + self.radius + (self.dx*t)) >= screen_width:
            difference = (self.x + self.radius + (self.dx*t)) - screen_width
            self.x = screen_width - self.radius - difference
            self.dx *= -1
            self.acceleration_x *= -1
            skipx = 1
        elif (self.x - self.radius + (self.dx*t)) <= 0:
            difference = -(self.x - self.radius + (self.dx*t)) 
            self.x = self.radius + difference
            self.dx *= -1
            self.acceleration_x *= -1
            skipx = 1
        #Update Y
        if (self.y + self.radius + (self.dy*t)) >= screen_height:
            difference = (self.y + self.radius + (self.dy*t)) - screen_height
            self.y = screen_height - self.radius - difference
            self.dy *= -1
            self.acceleration_y *= -1
            skipy = 1
        elif (self.y - self.radius + (self.dy*t)) <= 0:
            difference = -(self.y - self.radius + (self.dy*t)) 
            self.y = self.radius + difference
            self.dy *= -1
            self.acceleration_y *= -1
            skipy = 1

        if skipx:
            skipx = 0
        else:
            skipx = 0
            self.x += self.dx*t
        if skipy:
            skipy = 0
        else:
            skipy = 0
            self.y += self.dy*t

    def draw_circle(self):
        pygame.draw.circle(screen, self.RGB, (self.x, self.y), self.radius)
    
    def proportional_control(Kp):
        pass

#Create array for number of circles
circles = []
for i in range(number_of_circles):
    radius = 50
    #random.randint(5, 50)
    x, y, dx, dy, acceleration_x, acceleration_y, RGB = initial_conditions(radius)
    circles.append(circle(radius, x, y, dx, dy, acceleration_x, acceleration_y, RGB))



clock=pygame.time.Clock()
t = 0
mouse_down = 1
while running:
    start_time = time.time()
    clock.tick(200)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_down == 1:
            number_of_circles += 1
            print("Mouse clicked", pygame.mouse.get_pos()[0])
            x, y, dx, dy, acceleration_x, acceleration_y, RGB = initial_conditions(radius)
            circles.append(circle(radius, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 0, 0, acceleration_x, acceleration_y, RGB))
            mouse_down = 0
        if event.type == pygame.MOUSEBUTTONUP:
            circles[number_of_circles-1].dx = dx
            circles[number_of_circles-1].dy = dy
            mouse_down = 1
        if event.type == pygame.QUIT:
            running = False
            
    screen.fill((0, 0, 0))  # Fill the background with black
    for i in range(number_of_circles):
        circles[i].update_velocities()
        circles[i].update_positions()
        circles[i].draw_circle()
    pygame.display.flip()
    end_time = time.time()
    t = end_time-start_time

    if pygame.key.get_pressed()[pygame.K_v]:
        sys.exit()

pygame.quit()
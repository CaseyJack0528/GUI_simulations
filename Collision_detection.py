import pygame
import random
import math
import time
import sys

#######################################################################################
#Adjustable parameters
number_of_circles = 1 #Number of circles to spawn
random_position = 0 #Start in a random position? (1=yes, 0=no)
radius = 50
max_velocity = 1000
proportional_gain = 100
integral_gain = 100
collision_on = 1
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
        total_velocity = (self.dx**2 + self.dy**2)**(1/2)
        if total_velocity > max_velocity:
            theta = math.atan(self.dy/self.dx)
            if self.dx < 0:
                theta += math.pi
            self.dx = max_velocity*math.cos(theta)
            self.dy = max_velocity*math.sin(theta)

    def update_positions(self):
        global skipx
        global skipy

        #Update X
        if (self.x + self.radius + (self.dx*t)) >= screen_width:
            difference = (self.x + self.radius + (self.dx*t)) - screen_width
            self.x = screen_width - self.radius - difference
            self.dx *= -1
            skipx = 1
        elif (self.x - self.radius + (self.dx*t)) <= 0:
            difference = -(self.x - self.radius + (self.dx*t)) 
            self.x = self.radius + difference
            self.dx *= -1
            skipx = 1
        #Update Y
        if (self.y + self.radius + (self.dy*t)) >= screen_height:
            difference = (self.y + self.radius + (self.dy*t)) - screen_height
            self.y = screen_height - self.radius - difference
            self.dy *= -1
            skipy = 1
        elif (self.y - self.radius + (self.dy*t)) <= 0:
            difference = -(self.y - self.radius + (self.dy*t)) 
            self.y = self.radius + difference
            self.dy *= -1
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
    
    def proportional_control(self, Kp, mouseX, mouseY):
        error_x = Kp*(mouseX - self.x)
        error_y = Kp*(mouseY - self.y)
        self.acceleration_x = error_x
        self.acceleration_y = error_y
        
def collision_detection(circle1, circle2):
    global start_time
    circle1_x = circle1.x + circle1.dx*t
    circle1_y = circle1.y + circle1.dy*t
    circle2_x = circle2.x + circle2.dx*t
    circle2_y = circle2.y + circle2.dy*t
    circle1_v = ((circle1.dx-circle2.dx)**2 + (circle1.dy-circle2.dy)**2)**(1/2)
    circle2_v = ((circle2.dx-circle1.dx)**2 + (circle2.dy-circle1.dy)**2)**(1/2)

    distance = ((circle1_x-circle2_x)**2 + (circle1_y-circle2_y)**2)**(1/2)
    if distance<=(radius*2):
        x_midpoint = int(circle1.x - (circle1.x-circle2.x)/2)
        y_midpoint = int(circle1.y - (circle1.y-circle2.y)/2)
        #pygame.draw.circle(screen, (255, 0, 0), (x_midpoint, y_midpoint), 10)
        #print(x_midpoint, y_midpoint)
        #time.sleep(1)
        theta = math.atan2((screen_height-circle2.y)-(screen_height-circle1.y), circle2.x-circle1.x)
        print(theta)
        #sys.exit()
        if theta<0:
            theta+=2*math.pi
        if theta>2*math.pi:
            theta-=2*math.pi
        print(radians_to_degrees(theta))
        c1x = circle1.dx
        c1y = circle1.dy
        '''
        circle1.dx = circle2.dx
        circle1.dy = circle2.dy
        circle2.dx = c1x
        circle2.dy = c1y
        '''
        circle1.dx = (math.cos(theta))*circle1_v
        circle1.dy = (math.sin(theta))*circle1_v
        circle2.dx = (math.cos(theta))*circle2_v
        circle2.dy = (math.sin(theta))*circle2_v
        
        """
        if theta<(math.pi/2):
            circle1.dx = math.cos(theta)*circle2.dx
            circle1.dy = math.sin(theta)*circle2.dy
            circle2.dx = math.cos(theta)*c1x
            circle2.dy = math.sin(theta)*c1y
            
        #Quadrant 2
        if theta<(math.pi) and theta>=(math.pi/2):
            circle1.dx = math.cos(theta)*circle2.dx
            circle1.dy = math.sin(theta)*circle2.dy
            circle2.dx = math.cos(theta)*c1x
            circle2.dy = math.sin(theta)*c1y
            
        #Quadrant 3
        if theta<(3*math.pi/2) and theta>=(math.pi):
            circle1.dx = math.cos(theta)*circle2.dx
            circle1.dy = math.sin(theta)*circle2.dy
            circle2.dx = math.cos(theta)*c1x
            circle2.dy = math.sin(theta)*c1y
            
        #Quadrant 4
        if theta<(2*math.pi) and theta>=(3*math.pi/2):
            circle1.dx = math.cos(theta)*circle2.dx
            circle1.dy = math.sin(theta)*circle2.dy
            circle2.dx = math.cos(theta)*c1x
            circle2.dy = math.sin(theta)*c1y
        """
        circle2.x = circle2.x + circle2.dx*t
        circle2.y = circle2.y + circle2.dy*t
        circle2.x = circle2.x + circle2.dx*t
        circle2.y = circle2.y + circle2.dy*t
        #start_time = time.time()

def radians_to_degrees(radian):
    degrees = (radian/(math.pi*2))*360
    return degrees

#Create array for number of circles
circles = []
for i in range(number_of_circles):
    #random.randint(5, 50)
    x, y, dx, dy, acceleration_x, acceleration_y, RGB = initial_conditions(radius)
    circles.append(circle(radius, x, y, dx, dy, acceleration_x, acceleration_y, RGB))

clock=pygame.time.Clock()
t = 0
mouse_down = 1
PID_control = 0

while running:
    start_time = time.time()
    clock.tick(200)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            #If right mouse button pressed
            if event.button == 3 and mouse_down == 1:
                number_of_circles += 1
                x, y, dx, dy, acceleration_x, acceleration_y, RGB = initial_conditions(radius)
                circles.append(circle(radius, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 0, 0, acceleration_x, acceleration_y, RGB))
                mouse_down = 0
            #If left mouse button pressed
            if event.button == 1:
                PID_control = 1
                for i in range(number_of_circles):
                    circles[i].proportional_control(proportional_gain, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        if event.type == pygame.MOUSEBUTTONUP:
            #If right mouse button released
            if event.button == 3:
                circles[number_of_circles-1].dx = dx
                circles[number_of_circles-1].dy = dy
                mouse_down = 1
            #If left mouse button released
            if event.button == 1:
                PID_control = 0
                for i in range(number_of_circles):
                    circles[i].acceleration_x = 0
                    circles[i].acceleration_y = 0
        if event.type == pygame.QUIT:
            running = False
            
    screen.fill((0, 0, 0))  # Fill the background with black
    for i in range(number_of_circles):
        if PID_control == 1:
            circles[i].proportional_control(proportional_gain, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        circles[i].update_velocities()
        circles[i].update_positions()
        if collision_on == 1:
            for n in range(i+1, number_of_circles):
                collision_detection(circles[i], circles[n])
        circles[i].draw_circle()
    pygame.display.flip()
    end_time = time.time()
    t = end_time-start_time

    if pygame.key.get_pressed()[pygame.K_v]:
        sys.exit()

pygame.quit()
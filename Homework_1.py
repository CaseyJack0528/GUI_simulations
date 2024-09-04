import math
import pygame
import matplotlib.pyplot as plt

#################################################################
starting = (0, 2)
ending = (2, 0)
speed = 1 #how long to travel path in seconds
draw_vector = 1 #if path taken is to be drawn
#################################################################

radius = 10
screen_x_axis = 10
screen_y_axis = 5
tick_width = 10
tick_width = 5
arm_length = 1
arm_width = 5

time_stamps = []
joint_2_angle = []
joint_1_angle = []

pygame.init()
window_size = pygame.display.Info()
screen_width = window_size.current_w
screen_height = window_size.current_h
print(pygame.display.Info())

screen = pygame.display.set_mode((screen_width, screen_height))
running = True

def screen_axis(coordinates):
    x, y = coordinates
    x = x*screen_width/screen_x_axis
    y = screen_height - y*screen_height/screen_y_axis
    return (x, y)

def tick_marks():
    for i in range(0, screen_x_axis):
        pygame.draw.line(screen, (255, 0, 0), (int(i*screen_width/screen_x_axis), screen_height-tick_width), (int(i*screen_width/screen_x_axis), screen_height), width=tick_width)

    for i in range(0, screen_y_axis):
        pygame.draw.line(screen, (255, 0, 0), (0, screen_height - round(i*screen_height/screen_y_axis)), (tick_width, screen_height - round(i*screen_height/screen_y_axis)), width=tick_width)

def draw_path(start, end):
    pygame.draw.line(screen, (0, 255, 0), start, end)

#################################################################
#Circle object (end effector)
class circle:
    def __init__(self, radius, x_start, y_start, RGB):
        self.radius = radius
        self.x_start = x_start
        self.y_start = y_start
        self.x = x_start
        self.y = y_start
        self.RGB = RGB

    def update_positions(self):
        t = pygame.time.get_ticks()/1000
        if t/speed <= 1:
            self.x = pygame.math.lerp(self.x_start, ending_point[0], t/speed)
            self.y = pygame.math.lerp(self.y_start, ending_point[1], t/speed)
        return t

    def draw_circle(self):
        pygame.draw.circle(screen, self.RGB, (self.x, self.y), self.radius)
#################################################################
#Line object (link arms)
class line:
    def __init__(self, length, width):
        self.length = length
        self.width = width
        self.angle = 0
    
    def update_position(self, starting_point, ending_point, t):
        if t/speed <= 1:
            x = pygame.math.lerp(starting_point[0], ending_point[0], t/speed)
            y = pygame.math.lerp(starting_point[1], ending_point[1], t/speed)
        else:
            x = pygame.math.lerp(starting_point[0], ending_point[0], 1)
            y = pygame.math.lerp(starting_point[1], ending_point[1], 1)
        angle2 = math.acos(((x**2)+(y**2)-(2*(self.length**2)))/(2*self.length))
        self.angle = math.atan2(y, x) - math.atan2((math.sin(angle2)), (self.length+(self.length*math.cos(angle2))))
        if t<speed:
            joint_1_angle.append(self.angle)
        arm_x = self.length*math.cos(self.angle)
        arm_y = self.length*math.sin(self.angle)
        pygame.draw.line(screen, (255, 255, 0), screen_axis((0, 0)), screen_axis((arm_x, arm_y)), width=self.width)
        return (arm_x, arm_y)
    
    def update_second_position(self, starting_point, ending_point, t, arm_start):
        if t/speed <= 1:
            x = pygame.math.lerp(starting_point[0], ending_point[0], t/speed)
            y = pygame.math.lerp(starting_point[1], ending_point[1], t/speed)
        else:
            x = pygame.math.lerp(starting_point[0], ending_point[0], 1)
            y = pygame.math.lerp(starting_point[1], ending_point[1], 1)
        self.angle = math.acos(((x**2)+(y**2)-(2*(self.length**2)))/(2*self.length))
        if t<speed:
            joint_2_angle.append(self.angle)
            time_stamps.append(t)
        arm_x = x
        arm_y = y
        pygame.draw.line(screen, (255, 255, 0), screen_axis(arm_start), screen_axis((arm_x, arm_y)), width=self.width)
        

clock=pygame.time.Clock()
theta = math.atan2((ending[1]-starting[1]), (ending[0]-starting[0]))
distance = math.sqrt((ending[0] - starting[0]) ** 2 + (ending[1] - starting[1]) ** 2)

starting_point = screen_axis(starting)
ending_point = screen_axis(ending)

end_effector = circle(radius, starting_point[0], starting_point[1], (0, 0, 255))
link_arm = line(arm_length, arm_width)
link_arm_2 = line(arm_length, arm_width)

while running:
    clock.tick(200)
    screen.fill((0, 0, 0))  # Fill the background with black
    tick_marks()
    draw_path(starting_point, ending_point)
    t = end_effector.update_positions()
    end_effector.draw_circle()
    second_arm_start = link_arm.update_position(starting, ending, t)
    link_arm_2.update_second_position(starting, ending, t, second_arm_start)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    if pygame.key.get_pressed()[pygame.K_v]:
        running = False
        pygame.quit()
        break
        #sys.exit()

fig, ax = plt.subplots()
ax.plot(time_stamps, joint_1_angle, 'b', label='Joint 1 Angle')
ax.plot(time_stamps, joint_2_angle, 'r', label='Joint 2 Angle')
ax.legend()
plt.show()

pygame.quit()
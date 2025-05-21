import pygame
import random
import math
import sys
import numpy as np

pygame.init()
window_size = pygame.display.Info()
screen_width = window_size.current_w
screen_height = window_size.current_h
print(pygame.display.Info())
screen = pygame.display.set_mode((screen_width, screen_height))
running = True

class snowflake:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def snowfall(self):
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), 1)

snow_amount = 50
snowflakes = [0 for i in range(snow_amount)]

for flake in range(snow_amount):
    snowflakes[flake] = snowflake(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

mouse_down = 0

while running:
    screen.fill((0, 0, 0))  # Fill the background with black
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            #If left mouse button pressed
            if event.button == 1:
                mouse_down = 1
        if event.type == pygame.MOUSEBUTTONUP:
            #If left mouse button released
            if event.button == 1:
                mouse_down = 0


    if mouse_down == 1:
        snowflakes.append(snowflake(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
        snow_amount += 1

    
    for flake in range(snow_amount):
        i = random.randint(-1, 1)
        if snowflakes[flake].y != screen_height-1:
            if snowflakes[flake].y != screen_height and pygame.Surface.get_at(screen, (snowflakes[flake].x+i, snowflakes[flake].y+1)) != (255, 255, 255, 255):
                snowflakes[flake].y += 1
                snowflakes[flake].x = snowflakes[flake].x + i
        snowflakes[flake].snowfall()
            

    pygame.display.flip()
    if pygame.key.get_pressed()[pygame.K_v]:
        sys.exit()

pygame.quit()
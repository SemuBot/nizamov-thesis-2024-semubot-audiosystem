import pygame
import usb.core
from tuning import Tuning
import os
import math

#variables for the filter
arr = []
n = 0

pygame.init()
width, height = 3300, 1800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Moving Pupils")

dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
angle_array = []

if not dev:
    print("USB microphone not found.")
    exit()

Mic_tuning = Tuning(dev)

def moving_average(pos):
    """
    :param pos: The latest value that is passed to the filter
    :return: The filtered value
    """
    global arr, n
    
    if pos:
        arr.append(pos)
        n = n + 1
    
    if n > 0 and n < 12:
        filtered_val = sum(arr[::-1])/n
    else:
        filtered_val = sum((arr[::-1])[0:12])/12
    #print("Filter val: ", filtered_val)
        
        
    return filtered_val

def draw_eyes():
    eye_radius = 250
    pupil_radius = 80
    eye_distance = 1500 
    eye_y = height // 2

    left_eye_x = width // 2 - eye_distance // 2
    pygame.draw.circle(screen, (255, 255, 255), (left_eye_x, eye_y), eye_radius)

    right_eye_x = width // 2 + eye_distance // 2
    pygame.draw.circle(screen, (255, 255, 255), (right_eye_x, eye_y), eye_radius)
    
    # DOA
    direction = Mic_tuning.direction
    direction_filtered = moving_average(direction)

    # Calculate pupil x-coordinate based on DOA (left to right movement)
    pupil_x_left = left_eye_x - int(math.cos(math.radians(direction_filtered)) * (eye_radius - pupil_radius))
    pupil_x_right = right_eye_x - int(math.cos(math.radians(direction_filtered)) * (eye_radius - pupil_radius))
    # Draw pupils on the x-axis only
    pygame.draw.circle(screen, (0, 0, 0), (pupil_x_left, eye_y), pupil_radius)
    pygame.draw.circle(screen, (0, 0, 0), (pupil_x_right, eye_y), pupil_radius)

try:
    while not os.path.exists("recording_done.txt"):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Draw background
        screen.fill((0, 0, 0))

        # Draw eyes with moving pupils on the x-axis
        draw_eyes()

        # Update display
        pygame.display.flip()

except KeyboardInterrupt:
    pass

finally:
    pygame.quit()
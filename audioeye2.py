import pygame
import usb.core
from tuning import Tuning
import os
import math
import time

#speed constant
range_factor = 1 # Adjust this value to control the range of the pupils
rotation_speed_factor = 0.0001  # Adjust this value to control the rotation speed

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

def update_direction_target(current_direction, target_direction):
    direction_diff = target_direction - current_direction
    return current_direction + rotation_speed_factor * direction_diff


def moving_average(pos, n_values):
    """
    :param pos: The latest value that is passed to the filter
    :n_values: The integer after which we start popping out the unnecessary values from our array and account only for the newest n_values only
    :return: The filtered value
    """
    global arr, n
    
    if pos:
        arr.append(pos)
        n = n + 1

    if n > n_values:
        arr = arr[-n_values:]
        n = n_values

    if n > 0:
        filtered_val = sum(arr[::-1]) / n
    else:
        filtered_val = 0  # Or any other default value
        
    print("Filter val: ", filtered_val)
        
        
    return filtered_val

def draw_eyes():
    eye_radius = 250
    pupil_radius = 80
    eye_distance = 1500 
    eye_y = height // 2

    left_eye_x = width // 2 - eye_distance // 2
    right_eye_x = width // 2 + eye_distance // 2
    
    eye_image = pygame.image.load("eye.png")
    eye_image = pygame.transform.scale(eye_image, (eye_radius * 2, eye_radius * 2))

    screen.blit(eye_image, (left_eye_x - eye_radius, eye_y - eye_radius))
    screen.blit(eye_image, (right_eye_x - eye_radius, eye_y - eye_radius))
    
    # DOA
    direction = Mic_tuning.direction
    direction_filtered = moving_average(direction, 12)

    direction_filtered = update_direction_target(direction_filtered, Mic_tuning.direction)

    # Calculate pupil x-coordinate based on DOA (left to right movement)
    pupil_x_left = left_eye_x - int(range_factor * math.cos(math.radians(direction_filtered)) * (eye_radius - pupil_radius)) 
    pupil_x_right = right_eye_x - int(range_factor * math.cos(math.radians(direction_filtered)) * (eye_radius - pupil_radius)) 
    
    # Draw pupils on the x-axis using the same image
    pupil_image = pygame.image.load("eye.png")
    pupil_image = pygame.transform.scale(pupil_image, (pupil_radius * 2, pupil_radius * 2))

    screen.blit(pupil_image, (pupil_x_left - pupil_radius, eye_y - pupil_radius))
    screen.blit(pupil_image, (pupil_x_right - pupil_radius, eye_y - pupil_radius))

try:
    while not os.path.exists("recording_done.txt"):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill((0, 0, 0))

        draw_eyes()

        pygame.display.flip()

except KeyboardInterrupt:
    pass

finally:
    pygame.quit()
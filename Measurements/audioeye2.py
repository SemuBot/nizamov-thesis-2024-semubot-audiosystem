import pygame
import usb.core
from tuning import Tuning
import os
import math
import time

#speed constant
range_factor = 0.5 # Adjust this value to control the range of the pupils
rotation_speed_factor = 0.001  # Adjust this value to control the rotation speed

#variables for the filter
arr = []
n = 0

pygame.init()
width, height = 1920, 1080
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
# screen = pygame.display.set_mode((width, height), pygame.RESIZABLE | pygame.NOFRAME)
pygame.display.set_caption(" ")


#rescaling constants
eye_radius = 250
pupil_radius = 80
eye_distance = 650
eye_y = height // 2
lid_scale_factor = 1 * eye_distance / 2388  # Adjust as needed
lid_width = int(2388 * lid_scale_factor) * 2.135
lid_height = int(1668 * lid_scale_factor) * 2

dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
angle_array = []

if not dev:
    print("USB microphone not found.")
    exit()

Mic_tuning = Tuning(dev)

lid_image = pygame.image.load("lidst.png")
outline_image = pygame.image.load("outline.png")
# Draw pupils on the x-axis using an image with a transparent background
pupil_image = pygame.image.load("eyebb.png")  # Use an image with a transparent background

mouth_image = pygame.image.load("mouth.png")


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
    global pupil_image, eye_radius, pupil_radius, eye_distance, eye_y, lid_scale_factor, lid_width, lid_height

    left_eye_x = width // 2 - eye_distance // 2 - 55 #adjust x eye positions here, default -> 750
    right_eye_x = width // 2 + eye_distance // 2 + 145 #default -> 2650

    # Calculate the positions for lids and outlines in the center of the screen
    # Scale the lids based on their original size

    lid_image_scaled = pygame.transform.scale(lid_image, (lid_width, lid_height))

    outline_image_scaled = pygame.transform.scale(outline_image, (lid_width, lid_height))

    mouth_image_scaled = pygame.transform.scale(mouth_image, (lid_width/3, lid_height/6))

    # Draw scaled lids on top of the outlines
    screen.blit(lid_image_scaled, (270, 100))
    screen.blit(outline_image_scaled, (270, 100))
    screen.blit(mouth_image_scaled, (730, 700))
     
    # DOA
    direction = Mic_tuning.direction
    #direction_filtered = moving_average(direction, 2)

    #direction_filtered = update_direction_target(direction, Mic_tuning.direction)

    # Calculate pupil x-coordinate based on DOA (left to right movement)

    substi = int(range_factor * math.cos(math.radians(direction)) * (eye_radius - pupil_radius))
    pupil_x_left = left_eye_x - substi 
    pupil_x_right = right_eye_x - substi
    # if substi > 50:
    #         pupil_x_left = left_eye_x - (substi + 100)
    #         pupil_x_right = right_eye_x - (substi + 100)

    # print(substi)
    # print(pupil_x_left, pupil_x_right)
    # Adjust the y-coordinate to center the pupils within the lids
    pupil_y = eye_y - pupil_radius * 2 - (+65) #adjust y eye position here
    pupil_image = pygame.transform.scale(pupil_image, (pupil_radius * 2.95, pupil_radius * 2.95))
    screen.blit(pupil_image, (pupil_x_left - pupil_radius * 2, pupil_y))
    screen.blit(pupil_image, (pupil_x_right - pupil_radius * 2, pupil_y))

try:
    while not os.path.exists("recording_done.txt"):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.VIDEORESIZE:
                # Handle window resize event
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            

        screen.fill((255, 255, 255))

        draw_eyes()

        #pygame.display.flip()

        # # Copy the screen to a new surface
        # screen_copy = pygame.Surface((width, height))
        # screen_copy.blit(screen, (0, 0))
        # # Flip the new surface vertically
        # screen_copy = pygame.transform.flip(screen_copy, True, True)
        # # Update the original screen with the flipped surface
        # screen.blit(screen_copy, (0, 0))

        pygame.display.flip()

except KeyboardInterrupt:
    pass

finally:
    pygame.quit()
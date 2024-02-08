import dlib
import cv2
import face_recognition
import pygame
import usb.core
from tuning import Tuning
import os
import math
import time

# Speed constant
range_factor = 1  # Adjust this value to control the range of the pupils
rotation_speed_factor = 0.0001  # Adjust this value to control the rotation speed

# Variables for the filter
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

def draw_eyes(direction_filtered):
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

    # Calculate pupil x-coordinate based on DOA (left to right movement)
    pupil_x_left = left_eye_x - int(range_factor * math.cos(math.radians(direction_filtered)) * (eye_radius - pupil_radius))
    pupil_x_right = right_eye_x - int(range_factor * math.cos(math.radians(direction_filtered)) * (eye_radius - pupil_radius))

    # Draw pupils on the x-axis using the same image
    pupil_image = pygame.image.load("eye.png")
    pupil_image = pygame.transform.scale(pupil_image, (pupil_radius * 2, pupil_radius * 2))

    screen.blit(pupil_image, (pupil_x_left - pupil_radius, eye_y - pupil_radius))
    screen.blit(pupil_image, (pupil_x_right - pupil_radius, eye_y - pupil_radius))

# Start video capture for webcam - Specifying 0 as an argument fires up the webcam feed
video_capture = cv2.VideoCapture(0)

try:
    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Calling face_locations function on the converted frame.
        dets = face_recognition.face_locations(rgb_small_frame)
        # Loop over the identified locations to draw a rectangle on the face
        for (top, right, bottom, left) in dets:

            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            print((top + right + bottom + left) / 4)
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Calculate the average position of the face for filtering
            face_position = (top + right + bottom + left) / 4

            # Update direction based on the face position
            direction_filtered = moving_average(face_position, 20)
            direction_filtered = update_direction_target(direction_filtered, Mic_tuning.direction)

            # Display the resulting image
            cv2.imshow('Face_recognition', frame)

            # Draw eyes based on the filtered direction
            screen.fill((0, 0, 0))
            draw_eyes(direction_filtered)
            pygame.display.flip()

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    video_capture.release()
    cv2.destroyAllWindows()
    pygame.quit()

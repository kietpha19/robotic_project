#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import time


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()

# Initialize the motors.
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

# Initialize the drive base.
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

# Write your program here.
ev3.speaker.beep()

# Initialize the gyro sensor
gyro_sensor = GyroSensor(Port.S4)

# Function to make the robot go straight
def go_straight(speed, duration):
    initial_angle = gyro_sensor.angle()
    
    start_time = time.time()  # Get the current time

    while (time.time() - start_time) < duration / 1000.0:  # Convert duration to seconds
        # Adjust motor speeds based on gyro sensor reading
        error = gyro_sensor.angle() - initial_angle
        correction = error * 1.0  # Adjust the correction factor as needed

        left_motor.dc(speed - correction)
        right_motor.dc(speed + correction)

        wait(5)  # Wait for a short time

    # Stop the motors
    left_motor.stop()
    right_motor.stop()

# Example usage
#go_straight(50, 2000)  # Go straight at a speed of 50 for 2 seconds

# Calculate the distance per rotation based on your robot's wheel configuration
distance_per_rotation = 185  # Adjust based on your robot

# Function to make the robot go straight a certain distance using encoders
def go_straight_by_distance(speed, distance):
    initial_left_position = left_motor.angle()
    initial_right_position = right_motor.angle()
    
    rotations_needed = abs(distance / distance_per_rotation)

    initial_angle = gyro_sensor.angle()

    while True:
        # Adjust motor speeds based on gyro sensor reading
        error = gyro_sensor.angle() - initial_angle
        correction = error * 1.0  # Adjust the correction factor as needed

        left_motor.dc(speed - correction)
        right_motor.dc(speed + correction)

        left_position = left_motor.angle()
        right_position = right_motor.angle()
    
        left_distance = (left_position - initial_left_position) / 360.0 * distance_per_rotation
        right_distance = (right_position - initial_right_position) / 360.0 * distance_per_rotation
    
        average_distance = (left_distance + right_distance) / 2.0

        if abs(average_distance) >= abs(distance):
            break

        wait(10)

    # Stop the motors
    left_motor.stop()
    right_motor.stop()

# Constants for your robot
gyro_sensitivity = 3.0  # Adjust based on your gyro sensor
k_p = 5.0  # Proportional gain for gyro correction

# Function to turn the robot by a certain number of degrees using encoders and gyro correction
def turn_by_degrees(speed, degrees):
    initial_angle = gyro_sensor.angle()
    initial_left_position = left_motor.angle()
    initial_right_position = right_motor.angle()

    left_motor.dc(speed)
    right_motor.dc(-speed)  # Reverse the direction for the right motor to achieve a turn

    while True:
        current_angle = gyro_sensor.angle()
        angle_difference = current_angle - initial_angle
        if abs(angle_difference) >= abs(degrees):
            break

        # Calculate distance traveled using encoders
        left_distance = (left_motor.angle() - initial_left_position) / 360.0 * distance_per_rotation
        right_distance = (right_motor.angle() - initial_right_position) / 360.0 * distance_per_rotation
        average_distance = (left_distance + right_distance) / 2.0

        # Adjust motor speeds based on gyro sensor reading
        correction = angle_difference * k_p

        left_motor.dc(speed - correction)
        right_motor.dc(-speed - correction)

        wait(10)

    # Stop the motors
    left_motor.stop()
    right_motor.stop()

# Example usage to move 1000 mm
# go_straight_by_distance(50, 500)  # Go straight at a speed of 100 until it travels 1000 mm
# wait(1000) # wait 1 sec
# go_straight_by_distance(-50, 300)

turn_by_degrees(20, 90)
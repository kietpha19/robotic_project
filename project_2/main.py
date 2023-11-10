#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()
left_motor = Motor(Port.A)
right_motor = Motor(Port.D)
light_sensor = ColorSensor(Port.S1)

# Write your program here.
ev3.speaker.beep()

# Set the desired safe distance from the light source in arbitrary units
desired_distance = 10  # Adjust as needed

# Set the speed to approach the light source
approach_speed = 40  # Adjust as needed

while True:
    # Read the light intensity from the light sensor
    light_intensity = light_sensor.ambient()

    # Calculate an error based on the difference between the measured light intensity
    # and the desired light intensity (e.g., the light source intensity)
    desired_intensity = 50  # Adjust as needed
    error = desired_intensity - light_intensity

    # Calculate the motor speed difference based on the error
    motor_speed_difference = error

    # Adjust motor speeds for following and maintaining a safe distance
    left_motor.dc(approach_speed + motor_speed_difference)
    right_motor.dc(approach_speed - motor_speed_difference)

    wait(10)  # Adjust the delay as needed


    
    

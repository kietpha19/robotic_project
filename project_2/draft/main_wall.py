#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

from Controller import *

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()
left_motor = Motor(Port.A)
right_motor = Motor(Port.D)
sonar_sensor = UltrasonicSensor(Port.S3)
gyro_sensor = GyroSensor(Port.S4)

# Write your program here.
ev3.speaker.beep()

speed = 50
lower_threshold = 100
upper_threshold = 200
initial_angle = gyro_sensor.angle()


while True:
    distance = sonar_sensor.distance()
    print(distance)
    
    # wall following mode
    if distance <= 150:

        # Adjust motor speeds based on gyro sensor reading
        error = gyro_sensor.angle() - initial_angle
        correction = error * 1.2  

        if distance < lower_threshold:
            left_motor.dc(speed - correction)
            right_motor.dc(speed + correction + 6)
        elif distance > upper_threshold:
            left_motor.dc(speed - correction - 3)
            right_motor.dc(speed + correction)
        elif lower_threshold <= distance <= upper_threshold:
            left_motor.dc(speed - correction)
            right_motor.dc(speed + correction)

    left_motor.stop()
    right_motor.stop()




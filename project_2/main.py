#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from Controller import *

# Create your objects here.
# ev3 = EV3Brick()
# left_motor = Motor(Port.A)
# right_motor = Motor(Port.D)
# sonar_sensor = UltrasonicSensor(Port.S3)
# gyro_sensor = GyroSensor(Port.S4)

# # Write your program here.
# ev3.speaker.beep()
# lower = 80
# upper = 130
# out = 250

# def follow_wall():
#     speed = 30
#     initial_angle = gyro_sensor.angle()
#     while True:
#         distance = sonar_sensor.distance()
#         error = gyro_sensor.angle() - initial_angle
#         correction = error * 1.2  
#         if lower <= distance <= upper:
#             left_motor.dc(speed - correction)
#             right_motor.dc(speed + correction + 2)
#             print("correct")
#         elif distance < lower:
#             left_motor.dc(speed)
#             right_motor.dc(speed+5)
#             print("go out")
#         elif upper < distance < out:
#             left_motor.dc(speed+5)
#             right_motor.dc(speed)
#             print("go in")
#         else:
#             left_motor.stop()
#             right_motor.stop()

#         wait(10)


# follow_wall()

ev3.speaker.beep()
controller = Controller()
# controller.turn_to_fire()
controller.wander(1)
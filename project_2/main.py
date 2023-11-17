#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
#from Controller import *

# Create your objects here.
ev3 = EV3Brick()
# left_motor = Motor(Port.A)
# right_motor = Motor(Port.D)
# sonar_sensor = UltrasonicSensor(Port.S3)
# gyro_sensor = GyroSensor(Port.S4)
light_sensor = ColorSensor(Port.S1)
# fan_motor = Motor(Port.B)
touch_sensor = TouchSensor(Port.B)

while True:
    if touch_sensor.pressed():
        print("pressed")

ev3.speaker.beep()
controller = Controller()
# controller.extinguish()
# controller.turn_to_fire_180()
# controller.wander(1)

# while True:
#     print(light_sensor.ambient())
#     wait(10)

# fan_motor.run_time(speed = 300, time = 3000, wait = False)
# controller.turn("left")
# controller.turn("right")
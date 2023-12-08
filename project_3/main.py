#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from ArmController2 import *

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()


# Write your program here.
ev3.speaker.beep()

start = (1,10)
end = (8,15)

path = [(1,12), (7,17), (12,14), (1,12)]

controller = ArmController()
controller.draw_path(path)

# controller = ArmController()
# theta1, theta2 = controller.inv_kinematic(1,10)
# controller.turn_joint1(theta1)
# controller.turn_joint2(theta2)

# controller.pen("down")

# theta3, theta4 = controller.inv_kinematic(8,15)
# controller.turn_joint2(theta4-theta2, wait = False)
# controller.turn_joint1(theta3-theta1)



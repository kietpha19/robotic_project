#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

from Planner import PathPlanner
from Controller import Controller


# Create your objects here.
ev3 = EV3Brick()

# Write your program here.
ev3.speaker.beep()

# planner = PathPlanner()
# ins = planner.get_instruction("4d")
# planner.print_grid()
# print(ins)

test_ins = ["2 fw", "1 turn_pos_90", "2 bw"]
controller = Controller()
controller.execute_instruction(test_ins)






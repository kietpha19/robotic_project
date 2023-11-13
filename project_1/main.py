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

# planner = PathPlanner()
# ins = planner.get_instruction("4d")
# controller = Controller()
# controller.execute_instruction(ins)

# planner.print_grid()
# print(ins)

# print(ins)

test_ins = ["10 fw"]
controller = Controller()
controller.execute_instruction(test_ins)





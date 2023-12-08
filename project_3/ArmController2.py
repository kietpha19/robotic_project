from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from math import *

# arm configuration
l1 = 7
l2 = 15
joint1 = Motor(Port.D) # the shoulder
joint2 = Motor(Port.B) # the elbow
joint3 = Motor(Port.C) # the wrist
joint1_speed = 30
joint2_speed = 30

class ArmController:

    def pen(self, action = "down"):
        if action == "down":
            joint3.run_angle(50, 20)
        else:
            joint3.run_angle(50, -30)

    def rad2deg(self, theta):
        return theta*(180/pi)

    def turn_joint1(self, degree, wait = True):
        ratio = 90/38 # trial and error, maybe need to adjust
        joint1.run_angle(joint1_speed, degree*ratio,then=Stop.HOLD, wait = wait)
        
    
    def turn_joint2(self, degree, wait = True):
        ratio = 90/73 # trial and error, maybe need to adjust
        joint2.run_angle(joint2_speed, degree*ratio,then=Stop.HOLD, wait = wait)
    
    def inv_kinematic(self, x, y):
        theta2 = acos((x**2 + y**2 - l1**2 - l2**2)/(2*l1*l2)) 
        if x == 0:
            gamma = pi/2
        else:
            gamma = atan(y/x)
        alpha = acos((l1**2 + x**2 + y**2 - l2**2)/(2*l1*sqrt(x**2 + y**2)))
        if theta2 > 0:
            theta1 = gamma - alpha
        else:
            theta1 = gamma + alpha
        theta1 = self.rad2deg(theta1)
        theta2 = self.rad2deg(theta2)
        return (theta1, theta2)
    
    def draw_path(self, path):
        start_x, start_y = path[0]
        theta1, theta2 = self.inv_kinematic(start_x, start_y)

        # go to the initial position and pen down
        self.turn_joint1(theta1)
        self.turn_joint2(theta2)
        self.pen("down")
        wait(500)
        i = 1
        for x, y in path:
            print("line: ", i)
            i+=1
            next_theta1, next_theta2 = self.inv_kinematic(x, y)

            self.turn_joint2(next_theta2 - theta2, wait = False)
            self.turn_joint1(next_theta1 - theta1)

            theta1 = next_theta1
            theta2 = next_theta2

            wait(1500)
    
        self.pen("up")
        
            



       






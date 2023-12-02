from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from math import *
import threading

# arm configuration
l1 = 7
l2 = 11
joint1 = Motor(Port.D) # the shoulder
joint2 = Motor(Port.B) # the elbow
joint3 = Motor(Port.C) # the wrist
joint1_speed = 10
joint2_speed = 30

class ArmController:

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
    
    def interpolation(self, start, end, stepSize): 
        pathCoords = []
        distance = sqrt(pow((end[0]-start[0]),2)+pow((end[1]-start[1]),2))
        totalSteps= distance/stepSize

        # n is the amount of increments we want 
        n = 0
        x,y = -1,-1
        while (x,y) != end and n < distance:
            x = start[0] + (n/distance * (end[0] - start[0]))
            y = start[1] + (n/distance * (end[1]-start[1]))
            n+=stepSize # How much we want to increase by 

            pathCoords.append((x,y))
        pathCoords.append((x,y))
        return pathCoords
    
    def get_angle_steps(self, pathCoords):
        pathAngles = []
        for x, y in pathCoords:
            pathAngles.append(self.inv_kinematic(x, y))
        
        return pathAngles
    
    def draw_line(self, start, end, stepSize):
        pathCoords = self.interpolation(start, end, stepSize)
        pathAngles = self.get_angle_steps(pathCoords)

        startAngle = pathAngles[0]
        joint1_currAngle = startAngle[0]
        joint2_currAngle = startAngle[1]
     
        for joint1_nextAngle, joint2_nextAngle in pathAngles[1:]:
            theta1 = joint1_nextAngle - joint1_currAngle
            theta2 = joint2_nextAngle - joint2_currAngle
            print("theta1 = ", theta1)
            print("theta2 = ", theta2)

            # Create two threads
            thread1 = threading.Thread(target=self.turn_joint1, arg = [theta1])
            thread2 = threading.Thread(target=self.turn_joint2, arg = [theta2])

            # Start the threads
            thread1.start()
            thread2.start()

            # Wait for both threads to finish
            thread1.join()
            thread2.join()

            # update current joint angle
            joint1_currAngle = joint1_nextAngle
            joint2_currAngle = joint2_nextAngle


       






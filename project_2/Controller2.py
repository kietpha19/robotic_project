#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import random
import sys

ev3 = EV3Brick()
        
# Initialize the motors.
left_motor = Motor(Port.A)
right_motor = Motor(Port.D)

# Initialize the gyro sensor
light_sensor = ColorSensor(Port.S1)
left_touch_sensor = TouchSensor(Port.S2)
sonar_sensor = UltrasonicSensor(Port.S4)
right_touch_sensor = TouchSensor(Port.S3)

move_speed = 300
turn_speed = 50

# for the wall following
lower_wall_dist = 35
upper_wall_dist = 100
out_wall_dist = 200

state = "wander"

class Controller:
    def check(self):
        fire = light_sensor.color() == Color.YELLOW
        left_front = left_touch_sensor.pressed()
        right_front = right_touch_sensor.pressed()

        right = sonar_sensor.distance() <= out_wall_dist
        # print("fire: ", fire)
        # print("left front: ", left_front)
        # print("right front: ", right_front)
        # print("right: ", right)
        return fire, left_front, right_front, right
    
    def stop(self):
        # Stop the motors
        left_motor.stop()
        right_motor.stop()
        #wait(100)

    def forward(self):
        speed = move_speed
        
        while True:
            fire, left_front, right_front, right = self.check()
            if fire or left_front or right_front:
                self.stop()
                wait(1000)
                fire, left_front, right_front, right = self.check()
                return fire, left_front, right_front, right

            left_motor.run(speed)
            right_motor.run(speed+2)

            wait(10)
    
    # just backward a little bit
    def backward(self):
        speed = -move_speed
        while True:
            left_motor.run(speed)
            right_motor.run(speed-2)
            wait(500)
            if not left_touch_sensor.pressed() and not right_touch_sensor.pressed() :
                break
            
        self.stop()
              
    def turn(self, dir = "left", angle = 90):
        if dir == "right":
            angle = -angle

        if angle > 0:
            right_motor.run_angle(100, (angle*3 - 2)/2, wait = False) # turn left
            left_motor.run_angle(100, -(angle*3 - 2)/2)
        elif angle < 0:
            left_motor.run_angle(100, -(angle*3 + 2)/2, wait = False) # turn right
            right_motor.run_angle(100, (angle*3 + 2)/2)


    def wander(self, action = None):
        # ev3.speaker.say("wander")
        print("wander")
        if not action:
            action = random.randint(1,2)
        
        if action == 2:
            turn = random.randint(1, 4)
            if turn == 1:
                self.turn("left", 45)
            elif turn == 2:
                self.turn("right", 45)
            elif turn == 3:
                self.turn("left", 90)
            elif turn == 4:
                self.turn("right", 90)
        
        fire, left_front, right_front, right = self.forward()
        return fire, left_front, right_front, right
    
    def follow_wall(self):
        # ev3.speaker.say("wall following")
        print("follow wall")
        speed = move_speed
        while True:
            distance = sonar_sensor.distance()

            if lower_wall_dist <= distance <= upper_wall_dist:
                left_motor.run(speed)
                right_motor.run(speed+2)
                print("correct")
            elif distance < lower_wall_dist:
                left_motor.run(speed)
                right_motor.run(speed+10)
                print("go out")
            elif upper_wall_dist < distance < out_wall_dist:
                left_motor.run(speed+10)
                right_motor.run(speed)
                print("go in")
            else:
                self.stop()

            fire, left_front, right_front, right = self.check()
            if fire or left_front or right_front or not right:
                self.stop()
                return fire, left_front, right_front, right

    def extinguish(self):
        self.stop()
        print("extinguish")
        ev3.speaker.say("fire")
        sys.exit(0)
    
    def run(self):
        fire, left_front, right_front, right = self.wander(1)
        while True:
            if state == "wander":
                if fire:
                    self.extinguish()
                elif left_front and right_front and right:
                    self.backward()
                    self.turn("left")
                    fire, left_front, right_front, right = self.follow_wall()
                    state = "wall_following"
                elif left_front and right_front and not right:
                    self.backward()
                    turn = random.randint(1,2)
                    if turn == 1:
                        self.turn("left") 
                        fire, left_front, right_front, right = self.follow_wall()
                        state = "wall_following"
                    else:
                        self.turn("right")
                        fire, left_front, right_front, right = self.wander(1)
                elif left_front or right_front:
                    self.backward()
                    self.turn("right", 30)
                    if right:
                        fire, left_front, right_front, right = self.follow_wall()
                        state = "wall_following"
                    else:
                        fire, left_front, right_front, right = self.wander(1)
                else: #not front and not right
                    fire, left_front, right_front, right = self.wander(1)
            elif state == "wall_following":
                if fire:
                    self.extinguish()
                    #break;
                elif left_front and right_front and right:
                    self.backward()
                    self.turn("left")
                    fire, left_front, right_front, right = self.follow_wall()
                elif left_front and right_front and not right:
                    self.backward()
                    turn = random.randint(1,2)
                    if turn == 1:
                        self.turn("left") # should be random left or right
                        fire, left_front, right_front, right = self.follow_wall()
                    else:
                        self.turn("right")
                        fire, left_front, right_front, right = self.wander(1)
                        state = "wander"
                elif left_front or right_front:
                    self.backward()
                    self.turn("left", 30)
                    if right:
                        fire, left_front, right_front, right = self.follow_wall()
                    else:
                        fire, left_front, right_front, right = self.wander(1)
                        state = "wander"
                elif not left_front and not right_front and not right:
                    fire, left_front, right_front, right = self.wander()
                    state = "wander"

            
    

            
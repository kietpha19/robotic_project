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
fan_motor = Motor(Port.B)

# Initialize the gyro sensor
light_sensor = ColorSensor(Port.S1)
touch_sensor = TouchSensor(Port.S2)
sonar_sensor = UltrasonicSensor(Port.S3)
gyro_sensor = GyroSensor(Port.S4)

move_speed = 30
turn_speed = 50
light_threshold = 5 # maybe need to adjust

# for the wall following
lower_wall_dist = 80
upper_wall_dist = 130
out_wall_dist = 250

class Controller:
    def check(self):
        fire = light_sensor.ambient() >= light_threshold
        front = touch_sensor.pressed()
        right = sonar_sensor.distance() <= out_wall_dist
        return fire, front, right
    
    def stop(self):
        # Stop the motors
        left_motor.stop()
        right_motor.stop()
        #wait(100)

    def forward(self):
        speed = move_speed
        gyro_sensor.reset_angle(0)
        initial_angle = gyro_sensor.angle()
        while True:
            fire, front, right = self.check()
            if fire or front or right:
                self.stop()
                return fire, front, right
                
            # Adjust motor speeds based on gyro sensor reading
            error = gyro_sensor.angle() - initial_angle
            correction = error * 1.2  # Adjust the correction factor as needed

            left_motor.dc(speed - correction)
            right_motor.dc(speed + correction + 2)

            wait(10)
    
    # just backward a little bit
    def backward(self):
        speed = -move_speed
        initial_angle = gyro_sensor.angle()
        while True:
            # Adjust motor speeds based on gyro sensor reading
            error = gyro_sensor.angle() - initial_angle
            correction = error * 1.2  # Adjust the correction factor as needed

            left_motor.dc(speed - correction)
            right_motor.dc(speed + correction)
            if not touch_sensor.pressed():
                break
            
        self.stop()
              
    def turn(self, dir = "left"):
        if dir == "left":
            speed = turn_speed
        else:
            speed = -turn_speed
        
        gyro_sensor.reset_angle(0)
        while abs(gyro_sensor.angle()) < 90:
            right_motor.run(speed=speed)
            left_motor.run(speed=(-1 * speed))
            wait(10)  

        self.stop()

    def wander(self, action = None):
        ev3.speaker.say("wander")
        print("wander")
        if not action:
            action = random.randint(1,3)
        
        if action == 2:
            self.turn("left")
        elif action == 3:
            self.turn("right")
        
        fire, front, right = self.forward()

        if fire:
            self.extinguish()
        elif front and right:
            self.backward()
            self.turn("left")
            self.follow_wall()
        elif front and not right:
            # self.turn("left")
            # self.follow_wall()
            self.backward()
            self.turn(right)
            self.wander(1)
        elif not front and right:
            self.follow_wall()
        else: #not front and not right
            self.forward()
    
    def follow_wall(self):
        ev3.speaker.say("wall following")
        print("follow wall")
        speed = move_speed
        initial_angle = gyro_sensor.angle()
        while True:
            distance = sonar_sensor.distance()
            error = gyro_sensor.angle() - initial_angle
            correction = error * 1.2  
            if lower_wall_dist <= distance <= upper_wall_dist:
                left_motor.dc(speed - correction)
                right_motor.dc(speed + correction + 2)
                print("correct")
            elif distance < lower_wall_dist:
                left_motor.dc(speed)
                right_motor.dc(speed+3)
                print("go out")
            elif upper_wall_dist < distance < out_wall_dist:
                left_motor.dc(speed+2)
                right_motor.dc(speed)
                print("go in")
            else:
                self.stop()

            wait(10)

            fire, front, right = self.check()
            if fire or front or not right:
                self.stop()

            if fire:
                self.extinguish();
                #break;
            elif front and right:
                self.backward()
                self.turn("left")
                self.follow_wall()
            elif front and not right:
                self.backward()
                self.turn("right")
                self.wander(1)
            elif not front and not right:
                self.wander() # maybe change to turn right later

            wait(10)

    def turn_to_fire(self):
        speed = turn_speed
        gyro_sensor.reset_angle(0) # maybe comment this out
        #maybe increase this
        detected_ambient =  max(7, light_sensor.ambient())
        print("detected ambient: ", detected_ambient)    

        # maybe need to adjust these
        adjust = 2 
        count_greatter_thresh = 30
        count_smaller_thresh = 30
        count_greater = 0
        count_smaller = 0

        turn_left = True
        
        while abs(gyro_sensor.angle()) < 90:
            right_motor.run(speed=speed)
            left_motor.run(speed=(-1 * speed))
            wait(10)
            curr_ambient = light_sensor.ambient()
            print("ambient = ", curr_ambient)
            if curr_ambient > detected_ambient-adjust:
                count_greater +=1
            elif curr_ambient < detected_ambient: #maybe need to adjust
                count_smaller += 1

            # maybe need to add an or abs(gyro.angle()) > 45
            if turn_left and count_smaller > count_smaller_thresh:
                speed = -speed
                count_greater = 0
                count_smaller = - count_smaller
                turn_left = False
                wait(1000)
            if count_greater > count_greatter_thresh:
                break

            wait(10)
        
        self.stop()

    def move_closer_to_fire(self, max_light_thresh = 11):
        # keep going straight till closest position to the fire
        detected_ambient = light_sensor.ambient()
        speed = move_speed
        gyro_sensor.reset_angle(0)
        initial_angle = gyro_sensor.angle()
        while True:
            # Adjust motor speeds based on gyro sensor reading
            error = gyro_sensor.angle() - initial_angle
            correction = error * 1.2  # Adjust the correction factor as needed

            left_motor.dc(speed - correction)
            right_motor.dc(speed + correction + 2)

            curr_ambient = light_sensor.ambient()
            if curr_ambient >= max_light_thresh or curr_ambient < detected_ambient-2:
                break

            wait(10)

    def extinguish(self):
        ev3.speaker.say("extinguish")
        print("extinguish")
        self.move_closer_to_fire(max_light_thresh = 11)
        self.turn_to_fire()
        self.move_closer_to_fire(max_light_thresh = 17)

        fan_motor.run_time(speed = 300, time = 7000, wait = False)
        self.turn("left")
        self.turn("right")
        sys.exit(0)
    



    
    

            
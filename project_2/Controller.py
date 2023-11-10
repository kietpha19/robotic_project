#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import random

ev3 = EV3Brick()
        
# Initialize the motors.
left_motor = Motor(Port.A)
right_motor = Motor(Port.D)
fan_motor = Motor(Port.B)

# Initialize the gyro sensor
light_sensor = ColorSensor(port.S1)
touch_sensor = TouchSensor(port.S2)
sonar_sensor = UltrasonicSensor(port.S3)
gyro_sensor = GyroSensor(Port.S4)

move_speed = 50
turn_speed = 50
safe_distance = 500

class Controller:
    def check(self):
        fire = False
        front = False
        right = False
        if light_sensor.ambient() > 5:
            fire = True
        if touch_sensor.pressed():
            front = True
        if sonar_sensor.distance() <= 500:
            right = True
        return fire, front, right
    
    def stop(self):
        # Stop the motors
        left_motor.stop()
        right_motor.stop()

    def forward(self):
        speed = move_speed
        initial_angle = gyro_sensor.angle()
        while True:
            front, right = self.check()
            if front or right:
                break
            # Adjust motor speeds based on gyro sensor reading
            error = gyro_sensor.angle() - initial_angle
            correction = error * 1.2  # Adjust the correction factor as needed

            left_motor.dc(speed - correction)
            right_motor.dc(speed + correction)

            wait(10)

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

        right_motor.brake()
        left_motor.brake()

    def wander(self, action = None):
        if not action:
            action = random.randint(1,3)
        
        if action == 1:
            self.forward()
        elif action == 2:
            self.turn("left")
        else:
            self.turn("right")
        
        fire, front, right = self.check()
        if fire:
            self.extinguish()
        elif front and right:
            self.turn("left")
            self.follow_wall()
        elif front and not right:
            # self.turn("left")
            # self.follow_wall()
            self.turn(right)
            self.wander(1)
        elif not front and right:
            self.follow_wall()
        else: #not front and not right
            self.forward()
    
    def follow_wall(self):
        while True:
            distance = sonar_sensor.distance()
            error = distance - safe_distance
            proportional_gain = 2  # Adjust as needed
            motor_speed_difference = proportional_gain * error

            # Adjust motor speeds to maintain the desired distance
            motor_left.dc(move_speed + motor_speed_difference)
            motor_right.dc(move_speed - motor_speed_difference)

            fire, front, right = self.check()
            if fire:
                self.extinguish();
            elif front and right:
                self.turn("left")
            elif front and not right:
                self.wander(1)
            elif not front and not right:
                self.wander()

            wait(10)
    
    def extinguish(self):
        while True:
            # Read the light intensity from the light sensor
            light_intensity = light_sensor.ambient()

            # Calculate an error based on the difference between the measured light intensity
            # and the desired light intensity (e.g., the light source intensity)
            desired_intensity = 5  # Adjust as needed
            error = desired_intensity - light_intensity

            # Calculate the motor speed difference based on the error
            motor_speed_difference = error

            # Adjust motor speeds for following and maintaining a safe distance
            motor_left.dc(approach_speed + motor_speed_difference)
            motor_right.dc(approach_speed - motor_speed_difference)

            wait(10)  # Adjust the delay as needed


    
    

            
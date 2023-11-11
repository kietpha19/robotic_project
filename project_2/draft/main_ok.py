#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

from Controller import *
# from utils import *


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()
left_motor = Motor(Port.A)
right_motor = Motor(Port.D)
sonar_sensor = UltrasonicSensor(Port.S3)
gyro_sensor = GyroSensor(Port.S4)

# Write your program here.
ev3.speaker.beep()

speed = 50
lower_threshold = 150
upper_threshold = 250
initial_angle = gyro_sensor.angle()
control = Controller()
light_sensor = ColorSensor(Port.S1)

fire_threshold = 10
counter = 0
check_interval = 10

def turn(dir = "left"):
    
    turn_speed = 50
    if dir == "left":
        speed = turn_speed
    else:
        speed = -turn_speed
    
    gyro_sensor.reset_angle(0)
    prev_ambient = light_sensor.ambient()

    while abs(gyro_sensor.angle()) < 90:
        right_motor.run(speed=speed)
        left_motor.run(speed=(-1 * speed))
        wait(10)
        curr_ambient = light_sensor.ambient()
        print("ambient = ", curr_ambient)
        if curr_ambient - prev_ambient > 0 and curr_ambient >= 4:
            break
        else:
            prev_ambient = curr_ambient
        
    right_motor.brake()
    left_motor.brake()


def forward():
    speed = 50
    initial_angle = gyro_sensor.angle()
    prev_ambient = light_sensor.ambient()

    while True:

        curr_ambient = light_sensor.ambient()
        if curr_ambient - prev_ambient > 0 and curr_ambient >= 17:
            break
        else:
            prev_ambient = curr_ambient
        # Adjust motor speeds based on gyro sensor reading
        error = gyro_sensor.angle() - initial_angle
        correction = error * 1.2  # Adjust the correction factor as needed

        left_motor.dc(speed - correction)
        right_motor.dc(speed + correction)


while True:
    distance = sonar_sensor.distance()
    print("distance to right wall = ", distance)
    print("ambient light = ", light_sensor.ambient())

    # if light_sensor.ambient() >= 7+3 and turn_flag == 1:
    #     forward()
    #     break
    
    # wall following mode
    if distance <= 300:

        if counter % check_interval == 0:
            print("Check fire!")
            fire, front, right = control.check(fire_threshold)
            if fire == True:
                print("ambient light = ", light_sensor.ambient())
                print("found fire!")

                turn("left")

        # Adjust motor speeds based on gyro sensor reading
        error = gyro_sensor.angle() - initial_angle
        correction = error * 1.2  

        if distance < lower_threshold:
            left_motor.dc(speed - correction)
            right_motor.dc(speed + correction + 18)
        elif distance > upper_threshold:
            left_motor.dc(speed - correction - 3)
            right_motor.dc(speed + correction)
        elif lower_threshold <= distance <= upper_threshold:
            left_motor.dc(speed - correction)
            right_motor.dc(speed + correction)

        counter += 1

    left_motor.stop()
    right_motor.stop()

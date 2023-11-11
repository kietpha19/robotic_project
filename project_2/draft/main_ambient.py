#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()
left_motor = Motor(Port.A)
right_motor = Motor(Port.D)
sonar_sensor = UltrasonicSensor(Port.S3)
gyro_sensor = GyroSensor(Port.S4)
light_sensor = ColorSensor(Port.S1)

wait_time = 5
turn_speed = 50

# Write your program here.
ev3.speaker.beep()


def check_ambient_intensity():
    area_ambient = []
    for i in range(wait_time):
        area_ambient.append(light_sensor.ambient())
        wait(1000)
    return sum(area_ambient)/len(area_ambient)


def turn(dir = "left"):
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
        if curr_ambient - prev_ambient > 0 and curr_ambient >= 7:
            break
        else:
            prev_ambient = curr_ambient
        # print("avg of ambient = ", check_ambient_intensity())
        
    right_motor.brake()
    left_motor.brake()

turn("left")

# while True:

    # print("start scanning region")
    # print("avg of front ambient = ", check_ambient_intensity())
    # print("end scanning region")

    # turn("left")

    # print("start scanning region")
    # print("avg of left ambient = ", check_ambient_intensity())
    # print("end scanning region")

    # turn("right")
    # wait(100)
    # turn("right")

    # print("start scanning region")
    # print("avg of right ambient = ", check_ambient_intensity())
    # print("end scanning region")

    # break

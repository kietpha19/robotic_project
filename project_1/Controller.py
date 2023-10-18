#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from input import u

ev3 = EV3Brick()
        
# Initialize the motors.
left_motor = Motor(Port.A)
right_motor = Motor(Port.D)

# Initialize the gyro sensor
gyro_sensor = GyroSensor(Port.S4)

move_speed = 50
turn_speed = 50
move_offset = 0
turn_offset = 0

class Controller:
    
    # Function to make the robot go straight a certain distance using encoders
    # utilize propotional algorithm
    def go_straight_by_distance(self, speed, distance):
        distance_per_rotation = 185
        initial_left_position = left_motor.angle()
        initial_right_position = right_motor.angle()

        initial_angle = gyro_sensor.angle()

        while True:
            # Adjust motor speeds based on gyro sensor reading
            error = gyro_sensor.angle() - initial_angle
            correction = error * 1.2  # Adjust the correction factor as needed

            left_motor.dc(speed - correction)
            right_motor.dc(speed + correction)

            left_position = left_motor.angle()
            right_position = right_motor.angle()
        
            left_distance = (left_position - initial_left_position) / 360.0 * distance_per_rotation
            right_distance = (right_position - initial_right_position) / 360.0 * distance_per_rotation
        
            average_distance = (left_distance + right_distance) / 2.0

            if abs(average_distance) >= abs(distance):
                break

            wait(10)

        # Stop the motors
        left_motor.stop()
        right_motor.stop()
    
    def turn_by_degree(self, speed, angle):
        gyro_sensor.reset_angle(0)
        while abs(gyro_sensor.angle()) < angle:
            right_motor.run(speed=speed)
            left_motor.run(speed=(-1 * speed))
            wait(10)  

        right_motor.brake()
        left_motor.brake()
    
    def execute_instruction(self, instruction):
        ev3.speaker.beep()

        for ins in instruction:
            n, action = ins.split(' ')
            n = int(n)

            if action == "fw":
                self.go_straight_by_distance(move_speed, n*u*1000)
            elif action == "fw_d":
                self.go_straight_by_distance(move_speed, n*u*sqrt(2)*1000)
            elif action == "bw":
                self.go_straight_by_distance(-move_speed, n*u*1000)
            elif action == "bw_d":
                self.go_straight_by_distance(-move_speed, n*u*sqrt(2)*1000)
            elif action == "turn_pos_45":
                self.turn_by_degree(turn_speed, 45)
            elif action == "turn_neg_45":
                self.turn_by_degree(-turn_speed, 45)
            elif action == "turn_pos_90":
                self.turn_by_degree(turn_speed, 90)
            elif ins == "turn_neg_90":
                self.turn_by_degree(-turn_speed, 90)
            
            wait(1000)
        
        ev3.speaker.beep()

            









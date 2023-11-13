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

move_speed = 40
turn_speed = 50
move_offset = 10
turn_offset = 0

class Controller:
    gyro_sensor.reset_angle(0)
    # Function to make the robot go straight a certain distance using encoders
    # utilize propotional algorithm
    def go_straight_by_distance(self, speed, distance):
        distance_per_rotation = 185
        initial_left_position = left_motor.angle()
        initial_right_position = right_motor.angle()

        while True:
            error = gyro_sensor.angle()
            correction = 1.5 * error  # Proportional control only

            left_motor.dc(speed - correction)
            right_motor.dc(speed + correction + 1)

            left_position = left_motor.angle()
            right_position = right_motor.angle()

            left_distance = (left_position - initial_left_position) / 360.0 * distance_per_rotation
            right_distance = (right_position - initial_right_position) / 360.0 * distance_per_rotation

            average_distance = (left_distance + right_distance) / 2.0

            if abs(average_distance) >= abs(distance):
                break

        # Stop the motors
        left_motor.stop()
        right_motor.stop()
        
    
    def turn_by_degree(self, speed, angle):
        
        while abs(gyro_sensor.angle()) < angle:
            left_motor.run(speed=(-1 * speed))
            right_motor.run(speed=speed)
             
        left_motor.brake()
        right_motor.brake()
        gyro_sensor.reset_angle(0)

    
    def execute_instruction(self, instruction):
        ev3.speaker.beep()
        #gyro_sensor.reset_angle(0)
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
                #robot.turn(90)
            elif action == "turn_neg_90":
                self.turn_by_degree(-turn_speed, 90)
                #robot.turn(-90)
            
            wait(1000)
        
        ev3.speaker.beep()

            









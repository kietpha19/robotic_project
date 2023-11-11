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
        if curr_ambient - prev_ambient > 0 and curr_ambient >= 7:
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
        if curr_ambient - prev_ambient > 0 and curr_ambient >= 10:
            break
        else:
            prev_ambient = curr_ambient
        # Adjust motor speeds based on gyro sensor reading
        error = gyro_sensor.angle() - initial_angle
        correction = error * 1.2  # Adjust the correction factor as needed

        left_motor.dc(speed - correction)
        right_motor.dc(speed + correction)
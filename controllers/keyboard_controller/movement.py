from controller import Robot
from constants import *
from math import pi

def move_1_tile(robot, devices):
    
    revolutions = TILE_LENGTH / WHEEL #rev in radians
    
    left_wheel_revolutions = devices.ps_left.getValue()
    right_wheel_revolutions = devices.ps_right.getValue()

    left_wheel_revolutions += revolutions
    right_wheel_revolutions += revolutions

    devices.left_motor.setVelocity(SPEED)
    devices.right_motor.setVelocity(SPEED)

    devices.left_motor.setPosition(left_wheel_revolutions)
    devices.right_motor.setPosition(right_wheel_revolutions)
    PID_correction(robot, devices)

def read_sensors(robot, ps, number_of_reads):
    
    avg1_right_angle_sensor = 0    #ps1
    avg6_left_angle_sensor = 0     #ps6

    avg2_right_sensor = 0     #ps2
    avg5_left_sensor = 0     #ps5

    #read distance sensors
    for i in range(0,number_of_reads): #more scans for better accuracy
    
        avg1_right_angle_sensor += ps[1].getValue()
        avg6_left_angle_sensor += ps[6].getValue()

        avg2_right_sensor += ps[2].getValue()
        avg5_left_sensor += ps[5].getValue()

        robot.step(TIME_STEP) #simulation update

    #average score of sensors measurements
    avg1_right_angle_sensor = avg1_right_angle_sensor / number_of_reads
    avg6_left_angle_sensor = avg6_left_angle_sensor / number_of_reads
    
    avg2_right_sensor = avg2_right_sensor / number_of_reads
    avg5_left_sensor = avg5_left_sensor / number_of_reads

    left_wall = avg5_left_sensor > 80.0
    right_wall = avg2_right_sensor > 80.0


    return avg1_right_angle_sensor, avg6_left_angle_sensor, left_wall, right_wall

def PID_correction(robot, devices):
    
    while True:
        distance_left_now = devices.ps_left.getValue()
        distance_right_now = devices.ps_right.getValue()

        right_angle_sensor, left_angle_sensor, left_wall, right_wall = read_sensors(robot, devices.ps, 2)

        previous_error = 0.00
        error_integral = 0.00
        P = 0.005  #0.005
        I = 0.0008 #0.0005  0.0001
        D = 0.0005 # 0.0002
        Middle = 75
        
        if left_wall and right_wall:
        
            error = left_angle_sensor - right_angle_sensor
            error_integral += error
            error_derivative = (previous_error - error)
            previous_error = error
            MotorSpeed = P * error + I * error_integral + D * error_derivative
            if MotorSpeed > 0.2:
                MotorSpeed = 0.2
            elif MotorSpeed < -0.2:
                MotorSpeed = -0.2

            devices.left_motor.setVelocity(SPEED + MotorSpeed)
            devices.right_motor.setVelocity(SPEED - MotorSpeed)
        elif left_wall:
            error = left_angle_sensor - Middle
                
            error_integral += error
            error_derivative = (previous_error - error)
            previous_error = error
            MotorSpeed = P * error + I * error_integral + D * error_derivative
            if MotorSpeed > 0.06:
                MotorSpeed = 0.06
            elif MotorSpeed < -0.06:
                MotorSpeed = -0.06

            devices.left_motor.setVelocity(SPEED + MotorSpeed)
            devices.right_motor.setVelocity(SPEED - MotorSpeed)
        elif right_wall:
            error = right_angle_sensor - Middle
            
            error_integral += error
            error_derivative = (previous_error - error)
            previous_error = error
            MotorSpeed = P * error + I * error_integral + D * error_derivative
            if MotorSpeed > 0.06:
                MotorSpeed = 0.06
            elif MotorSpeed < -0.06:
                MotorSpeed = -0.06

            devices.left_motor.setVelocity(SPEED - MotorSpeed)
            devices.right_motor.setVelocity(SPEED + MotorSpeed)
    
        distance_left_later = devices.ps_left.getValue()
        distance_right_later = devices.ps_right.getValue()

        if (distance_left_now == distance_left_later) and (distance_right_now == distance_right_later):
            break

def turn(robot, move_direction, devices):

    revolutions = (pi/2) * AXLE / 2 / WHEEL # in radians

    left_wheel_revolutions = devices.ps_left.getValue()
    right_wheel_revolutions = devices.ps_right.getValue()

    devices.left_motor.setVelocity(SPEED * 0.33)
    devices.right_motor.setVelocity(SPEED * 0.33)

    if(move_direction == 'right'):
        left_wheel_revolutions += revolutions
        right_wheel_revolutions -= revolutions
        devices.left_motor.setPosition(left_wheel_revolutions)
        devices.right_motor.setPosition(right_wheel_revolutions)
    elif(move_direction == 'left'):
        left_wheel_revolutions -= revolutions
        right_wheel_revolutions += revolutions
        devices.left_motor.setPosition(left_wheel_revolutions)
        devices.right_motor.setPosition(right_wheel_revolutions)
    elif(move_direction == 'back'):
        revolutions *= 2
        left_wheel_revolutions += revolutions
        right_wheel_revolutions -= revolutions
        devices.left_motor.setPosition(left_wheel_revolutions)
        devices.right_motor.setPosition(right_wheel_revolutions)


    while True:
        distance_left_now = devices.ps_left.getValue()
        distance_right_now = devices.ps_right.getValue()

        robot.step(TIME_STEP)

        distance_left_later = devices.ps_left.getValue()
        distance_right_later = devices.ps_right.getValue()

        if (distance_left_now == distance_left_later) and (distance_right_now == distance_right_later):
            break

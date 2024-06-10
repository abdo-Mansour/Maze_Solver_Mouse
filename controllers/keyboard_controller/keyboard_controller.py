"""keyboard_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor

from controller import Robot, Keyboard
from constants import *
import movement
# create the Robot instance.
robot = Robot()


# get the time step of the current world.
TIME_STEP = int(robot.getBasicTimeStep())

class Devices:
    def __init__(self, robot : Robot) -> None:
        self.left_motor = robot.getDevice('left wheel motor')
        self.right_motor = robot.getDevice('right wheel motor')

        self.left_motor.setVelocity(SPEED)
        self.right_motor.setVelocity(SPEED)

        self.ps_left = robot.getDevice("left wheel sensor")
        self.ps_left.enable(TIME_STEP)
        self.ps_right = robot.getDevice("right wheel sensor")
        self.ps_right.enable(TIME_STEP)

        self.ps = [''] * 8
        ps_names = (
            "ps0", "ps1", "ps2", "ps3",
                "ps4", "ps5", "ps6", "ps7"
        )
        for i in range(len(ps_names)):
            self.ps[i] = robot.getDevice(ps_names[i])
            self.ps[i].enable(TIME_STEP)
        
devices = Devices(robot)
moves = {'W' : "forward", 'A' : 'left', 'S' : 'back', 'D' : 'right'}
# Main loop:
def main():
    keyboard = Keyboard()
    keyboard.enable(TIME_STEP)
    while robot.step(TIME_STEP) != -1:

        key = keyboard.get_key()
        if key in moves:
            print("hello")
            match key:
                case 'W':
                    print(key)
                    movement.move_1_tile(robot, devices)
                case 'A' | 'S' | 'D':
                    print(key)
                    movement.turn(robot, moves[key], devices)
main()
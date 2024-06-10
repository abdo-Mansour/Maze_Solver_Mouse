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
        self.robot = robot
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
        
    def detect_side_walls(self):
        right_sensor = self.ps[2].getValue()
        left_sensor = self.ps[5].getValue()
        left_wall = left_sensor > 80.0
        right_wall = right_sensor > 80.0

        front_wall = self.ps[0].getValue() > 80.0 or self.ps[7].getValue() > 80.0
        back_wall = self.ps[3].getValue() > 80.0 or self.ps[4].getValue() > 80.0
        return front_wall, right_wall, back_wall, left_wall

def main():
    from dfs import Explorer
    dfs = Explorer(robot)
    dfs.main()
main()
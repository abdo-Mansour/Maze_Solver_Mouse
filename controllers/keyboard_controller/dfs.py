from constants import *
from controller import Robot, Keyboard

from movement import move_1_tile, turn, Oriantation


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
        return right_wall, back_wall, left_wall, front_wall

class Cell:
	def __init__(self, right_wall, down_wall, left_wall, up_wall,) -> None:
		"""
		Initialize a Cell object with walls.
		
		:param right_wall: Boolean indicating if there is a wall on the right side.
		:param down_wall: Boolean indicating if there is a wall on the lower side.
		:param left_wall: Boolean indicating if there is a wall on the left side.
		:param up_wall: Boolean indicating if there is a wall on the upper side.
		"""
		self.up_wall = up_wall
		self.right_wall = right_wall
		self.down_wall = down_wall
		self.left_wall = left_wall
		self.visited = False

class Grid:
	def __init__(self, rows, cols) -> None:
		"""
		Initialize a Grid object with a specified number of rows and columns.
		
		:param rows: Number of rows in the grid.
		:param cols: Number of columns in the grid.
		"""
		
		self.rows = rows
		self.cols = cols
		self.grid = [[None for _ in range(cols)] for _ in range(rows)]
	def add_cell(self, row, col, cell):
		"""
        Add a Cell object to the grid at the specified row and column.
        
        :param row: Row index where the cell should be added.
        :param col: Column index where the cell should be added.
        :param cell: The Cell object to add to the grid.
        :raises IndexError: If the specified row or column is out of grid bounds.
        """
		if 0 <= row < self.rows and 0 <= col < self.cols:
			self.grid[row][col] = cell
		else:
			raise IndexError("Cell position out of grid bounds")
	def get_cell(self, row, col):
		"""
		Retrieve the Cell object from the grid at the specified row and column.
		
		:param row: Row index of the cell to retrieve.
		:param col: Column index of the cell to retrieve.
		:return: The Cell object at the specified position, or None if the cell is undiscovered.
		:raises IndexError: If the specified row or column is out of grid bounds.
		"""
		# Check if the specified position is within the bounds of the grid
		if 0 <= row < self.rows and 0 <= col < self.cols:
			# Return the cell at the specified position in the grid
			return self.grid[row][col]
		else:
			# Raise an error if the position is out of bounds
			raise IndexError("Cell position out of grid bounds")

	def display_grid(self):
		"""
		Display the current state of the grid.
		
		Prints the grid to the console, showing None for undiscovered cells
		and the Cell objects otherwise.
		"""
		for row in range(self.rows):
			upper_row = ""
			middle_row = ""
			lower_row = ""

			for col in range(self.cols):
				cell = self.grid[row][col]

				if cell is None:
					# Represent undiscovered cell
					upper_row += "   "
					middle_row += "   "
					lower_row += "   "
				else:
					# Top border
					upper_row += "+" if cell.up_wall else " "
					upper_row += "---" if cell.up_wall else "   "
					upper_row += "+" if cell.up_wall else " "

					# Middle part
					middle_row += "|" if cell.left_wall else " "
					middle_row += "   "
					middle_row += "|" if cell.right_wall else " "

					# Bottom border
					lower_row += "+" if cell.down_wall else " "
					lower_row += "---" if cell.down_wall else "   "
					lower_row += "+" if cell.down_wall else " "

			print(upper_row)
			print(middle_row)
			print(lower_row)


class Explorer:
	def __init__(self, robot: Robot) -> None:
		self.grid = Grid(ROWS, COLUMNS)
		self.robot = robot
		self.devices = Devices(robot)
		self.position = START_POSITION
		self.oriantation = START_ORIANTATION
	def explore_current_cell(self):
		detected_walls: tuple = self.devices.detect_side_walls()
		cell = Cell(detected_walls[(0 - self.oriantation - 1) % 4],
					detected_walls[(1 - self.oriantation - 1) % 4],
					detected_walls[(2 - self.oriantation - 1) % 4],
					detected_walls[(3 - self.oriantation - 1) % 4]
			)
		self.grid.add_cell(*self.position, cell)
	def move_forward(self):
		move_1_tile(self.robot, self.devices)
		if self.oriantation == 0:
			self.position = (self.position[0], self.position[1] + 1)
		if self.oriantation == 1:
			self.position = (self.position[0] + 1, self.position[1])
		if self.oriantation == 2:
			self.position = (self.position[0], self.position[1] - 1)
		if self.oriantation == 3:
			self.position = (self.position[0] - 1, self.position[1])
	def turn(self, dir):
		turn(self.robot, dir, self.devices)
		if dir == 'left': self.oriantation = (self.oriantation-1) % 4
		if dir == 'back': self.oriantation = (self.oriantation+2) % 4
		if dir == 'right': self.oriantation = (self.oriantation+1) % 4
	def is_valid_move(self, r, c):
		return (r >= 0 and r < self.grid.rows) and (c >= 0 and c < self.grid.cols)
	def main(self):
		moves = {'W' : "forward", 'A' : 'left', 'S' : 'back', 'D' : 'right'}
		keyboard = Keyboard()
		keyboard.enable(TIME_STEP)
		while self.robot.step(TIME_STEP) != -1:

			key = keyboard.get_key()
			if key in moves:
				if(key == 'W'):
					print(key)
					self.move_forward()
				elif(key == 'A' or key == 'S' or key == 'D'):
					print(key)
					self.turn(moves[key])
				self.explore_current_cell()
				self.grid.display_grid()
	def backtrack(self, pos):
		



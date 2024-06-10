from constants import *
import copy
from controller import Robot, Keyboard
from draw_maze import MazeView
from movement import move_1_tile, turn, Oriantation, move_front_correct


class Devices:
	def __init__(self, robot : Robot) -> None:
		self.robot = robot
		self.left_motor = robot.getDevice('left wheel motor')
		self.right_motor = robot.getDevice('right wheel motor')

		self.left_motor.setVelocity(SPEED)
		self.right_motor.setVelocity(SPEED)
		self.tof = robot.getDevice("tof")
		self.tof.enable(TIME_STEP)
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
		self.walls = [right_wall, down_wall, left_wall, up_wall]
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
	def get_cell(self, row, col) -> Cell:
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
			raise IndexError("Cell position out of grid bounds, " + str((row, col)))

	def clear_visited(self):
		for i in range(self.rows):
			for j in range(self.cols):
				self.grid[i][j].visited = False

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

		self.all_paths = []

		self.maze_visualizer = MazeView()
		self.maze_visualizer.init_maze(self.grid)

	def explore_current_cell(self):
		detected_walls: tuple = self.devices.detect_side_walls()
		cell = Cell(detected_walls[(0 - self.oriantation - 1) % 4],
					detected_walls[(1 - self.oriantation - 1) % 4],
					detected_walls[(2 - self.oriantation - 1) % 4],
					detected_walls[(3 - self.oriantation - 1) % 4]
			)

		cell.visited = True
		self.grid.add_cell(*self.position, cell)
		### Update maze visualizer ###############
		self.maze_visualizer.update_maze_explored(self.position,self.grid)
		###########################################

	def move_forward(self):
		move_1_tile(self.robot, self.devices)
		self.position = self.calc_new_pos(self.position, self.oriantation)

	def calc_new_pos(self, pos, oriantation):
		if oriantation == 0:
			pos = (pos[0], self.position[1] + 1)
		if oriantation == 1:
			pos = (pos[0] + 1, pos[1])
		if oriantation == 2:
			pos = (pos[0], pos[1] - 1)
		if oriantation == 3:
			pos = (pos[0] - 1, pos[1])
		return pos
	
	def turn(self, dir):
		turn(self.robot, dir, self.devices)
		if dir == 'left': self.oriantation = (self.oriantation-1) % 4
		if dir == 'back': self.oriantation = (self.oriantation+2) % 4
		if dir == 'right': self.oriantation = (self.oriantation+1) % 4

	def face_towards(self, towards):
		if abs(towards - self.oriantation) == 2:
			self.turn('back')
		if abs(towards - self.oriantation)  < 4 - abs(towards - self.oriantation):
			while self.oriantation != towards:
				self.turn('left')
		else:
			while self.oriantation != towards:
				self.turn('right')
		return
	
	def relative_direction(self, from_pos, to_pos):
		row_diff = from_pos[0] - to_pos[0]
		col_diff = from_pos[1] - to_pos[1]
		if row_diff != 0:
			return Oriantation.UP if row_diff > 0 else Oriantation.DOWN
		return Oriantation.LEFT if col_diff > 0 else Oriantation.RIGHT
	
	def is_valid_move(self, r, c):
		return (r >= 0 and r < self.grid.rows) and (c >= 0 and c < self.grid.cols)
	
	def find_all_paths(self, curr_pos, current_path):
		if curr_pos == GOAL_POSITION:
			print("وصلت")
			current_path.append(curr_pos)
			self.all_paths.append(current_path.copy())
			return

		curr_cell = self.grid.get_cell(*curr_pos)
		if curr_cell.visited:
			return

		curr_cell.visited = True
		current_path.append(curr_pos)
		if not curr_cell.up_wall:
			new_pos = (curr_pos[0] - 1, curr_pos[1])
			if self.is_valid_move(*new_pos):
				self.find_all_paths(new_pos, current_path)

		if not curr_cell.right_wall:
			new_pos = (curr_pos[0], curr_pos[1] + 1)
			if self.is_valid_move(*new_pos):
				self.find_all_paths(new_pos, current_path)

		if not curr_cell.down_wall:
			new_pos = (curr_pos[0] + 1, curr_pos[1])
			if self.is_valid_move(*new_pos):
				self.find_all_paths(new_pos, current_path)

		if not curr_cell.left_wall:
			new_pos = (curr_pos[0], curr_pos[1] - 1)
			if self.is_valid_move(*new_pos):
				self.find_all_paths(new_pos, current_path)
		
		del current_path[-1]
		# curr_cell.visited = False


		# valid_directions = [i for i in range(4) if not curr_cell.walls[i]]
		# for dir in valid_directions:
		# 	current_path.append(curr_pos)
		# 	new_pos = self.calc_new_pos(curr_pos, dir)
		# 	print(new_pos)
		# 	self.find_all_paths(new_pos, current_path)
		# 	del current_path[-1]
		

		


	def main(self):
		moves = {'W' : "forward", 'A' : 'left', 'S' : 'back', 'D' : 'right'}
		keyboard = Keyboard()
		keyboard.enable(TIME_STEP)


		self.robot.step(TIME_STEP)
		tmp_path = []
		self.backtrack(self.position, tmp_path)

		self.grid.clear_visited()
		self.find_all_paths(START_POSITION, [])
		print(self.all_paths)
		# self.maze_visualizer.done()

		# while self.robot.step(TIME_STEP) != -1:

		# 	key = keyboard.get_key()
		# 	if key in moves:
		# 		if(key == 'W'):
		# 			print(key)
		# 			self.move_forward()
		# 		elif(key == 'A' or key == 'S' or key == 'D'):
		# 			print(key)
		# 			self.turn(moves[key])
		# 		self.explore_current_cell()
		# 		self.grid.display_grid()
		

	def backtrack(self, pos, curr_path):
		self.explore_current_cell()
		detected_walls = self.devices.detect_side_walls()
		if detected_walls[3]:
			print("front wall detected")
			move_front_correct(self.robot, self.devices)
		current_cell = self.grid.get_cell(*pos)
		if pos == GOAL_POSITION:
			self.all_paths.append((copy.deepcopy(curr_path), len(curr_path)))

		current_cell.visited = True
		valid_directions = [i for i in range(4) if not current_cell.walls[i]]
		for dir in valid_directions:
			new_pos = self.calc_new_pos(pos, dir)
			#valid if new_pos is None
			if self.is_valid_move(*new_pos) and self.grid.get_cell(*new_pos) is None:
				self.face_towards(dir)
				self.move_forward()

				# curr_path.append(new_pos)
				self.backtrack(new_pos, curr_path)
				# del curr_path[-1]

				#face toward pos from new_pos
				back_dir = self.relative_direction(new_pos, pos)
				self.face_towards(back_dir)
				self.move_forward()
				
		return


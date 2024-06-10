from constants import *
from controller import Robot
from movement import move_1_tile, turn, Oriantation


class Cell:
	def __init__(self, up_wall, right_wall, down_wall, left_wall) -> None:
		"""
		Initialize a Cell object with walls.
		
		:param up_wall: Boolean indicating if there is a wall on the upper side.
		:param right_wall: Boolean indicating if there is a wall on the right side.
		:param down_wall: Boolean indicating if there is a wall on the lower side.
		:param left_wall: Boolean indicating if there is a wall on the left side.
		"""
		self.up_wall = up_wall
		self.right_wall = right_wall
		self.down_wall = down_wall
		self.left_wall = left_wall



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
		for row in self.grid:
			print(row)


def dfs_main(robot: Robot, devices):
	current_position = (0,0) # start position of robot
	current_oriantatin = Oriantation.RIGHT




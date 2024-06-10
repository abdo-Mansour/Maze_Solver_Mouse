from turtle import *
# import var
from constants import *

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
		for row in self.grid:
			print(row)


def init_maze(maze_map,cell_size):
    BORDERS = 100
    WIDTH = BORDERS + cell_size * COLUMNS
    HEIGHT = BORDERS + cell_size * ROWS
    setup(WIDTH, HEIGHT) #size and position on screen

    maze = Turtle()
    maze.hideturtle()
    tracer(False)
    maze.color('black')
    maze.width(1)
    
    grid = Turtle()
    grid.hideturtle()
    grid.color('black')
    grid.width(1)

    text = Turtle()
    text.hideturtle()
    text.width(1)

    #draw grid
    start_y , start_x = -(HEIGHT-BORDERS) // 2 , -(WIDTH-BORDERS) // 2 
    end_y   , end_x   = (HEIGHT-BORDERS) // 2 , (WIDTH-BORDERS) // 2 
    for y in range(start_y, end_y, cell_size):
        for x in range(start_x, end_x, cell_size):
            line(x, y + cell_size, x + cell_size, y + cell_size, grid)
            line(x + cell_size, y, x + cell_size, y + cell_size, grid)
            line(x, y, x + cell_size, y, grid)
            line(x, y, x, y + cell_size, grid)

    maze.width(5)
    #draw walls
    i = 0
    j = 0
    for y in range(start_y, end_y, cell_size):
        i = 0
        for x in range(start_x, end_x, cell_size):
            draw_wall(maze_map.grid[j][i], x, y, cell_size, maze)
            
            i += 1
        j+=1

    return text, maze

def line(start_x, start_y, end_x, end_y, t):
    t.up()
    t.goto(start_x, start_y)
    t.down()
    t.goto(end_x, end_y) 
    t.up()
    t.goto(start_x, start_y)
    t.down()
    t.goto(end_x, end_y) 
    


def draw_wall(cell, x, y, size, t):
    if not cell.visited:
        return
    
    if cell.up_wall:
        draw_top(x, y, size, t)
    if cell.down_wall:
        draw_bottom(x, y, size, t)
    if cell.right_wall:
        draw_right(x, y, size, t)
    if cell.left_wall:
        draw_left(x, y, size, t)

def draw_top(x, y, size, t):
    line(x, y + size, x + size, y + size, t) # up horizontal line (top)

def draw_bottom(x, y, size, t):
    line(x, y, x + size, y, t) # down horizontal line (down)
    
def draw_right(x, y, size, t):
    line(x + size, y, x + size, y + size, t) # right vertical line (right)

def draw_left(x, y, size, t):
    line(x, y, x, y + size, t) # left vertical Line (left)



def update_maze_explored(visited_cell,cell_size,maze_map,t):
    pass

# initlize a sudo map

def draw_point(visited_cell,t):
    pass

def init_map():
    maze_map = Grid(ROWS, COLUMNS)
    for i in range(ROWS):
        for j in range(COLUMNS):
            cell = Cell(False, True, False, False)
            cell.visited = True
            maze_map.add_cell(i, j, cell)
    return maze_map

def main():
    maze_map = init_map()
    text, maze = init_maze(maze_map, 60)
    done()

main()
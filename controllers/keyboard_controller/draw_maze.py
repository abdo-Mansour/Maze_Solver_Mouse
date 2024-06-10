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




class MazeView:
    def __init__(self,cell_size = 60) -> None:
        self.BORDERS = 100
        self.cell_size = cell_size
        self.WIDTH = self.BORDERS + cell_size * COLUMNS
        self.HEIGHT = self.BORDERS + cell_size * ROWS
        self.start_y , self.start_x = -(self.HEIGHT-self.BORDERS) // 2 , -(self.WIDTH-self.BORDERS) // 2 
        self.end_y   , self.end_x   = (self.HEIGHT-self.BORDERS) // 2 , (self.WIDTH-self.BORDERS) // 2 
        
    def init_maze(self,maze_map):
        
        setup(self.WIDTH, self.HEIGHT) #size and position on screen

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
        
        for y in range(self.start_y, self.end_y, self.cell_size):
            for x in range(self.start_x, self.end_x, self.cell_size):
                self.line(x, y + self.cell_size, x + self.cell_size, y + self.cell_size, grid)
                self.line(x + self.cell_size, y, x + self.cell_size, y + self.cell_size, grid)
                self.line(x, y, x + self.cell_size, y, grid)
                self.line(x, y, x, y + self.cell_size, grid)

        maze.width(5)

        #draw walls
        i = 0
        j = 0
        for y in range(self.start_y, self.end_y, self.cell_size):
            i = 0
            for x in range(self.start_x, self.end_x, self.cell_size):
                self.draw_wall(maze_map.grid[j][i], x, y, maze)
                i+=1
            j+=1

        return text, maze

    def line(self,start_x, start_y, end_x, end_y, t):
        t.up()
        t.goto(start_x, start_y)
        t.down()
        t.goto(end_x, end_y) 
        t.up()
        t.goto(start_x, start_y)
        t.down()
        t.goto(end_x, end_y) 
        


    def draw_wall(self,cell, x, y, t):
        if not cell.visited:
            return
        
        if cell.up_wall:
            self.draw_top(x, y, t)
        if cell.down_wall:
            self.draw_bottom(x, y, t)
        if cell.right_wall:
            self.draw_right(x, y, t)
        if cell.left_wall:
            self.draw_left(x, y, t)

    def draw_top(self,x, y, t):
        self.line(x, y + self.cell_size, x + self.cell_size, y + self.cell_size, t) # up horizontal line (top)

    def draw_bottom(self,x, y, t):
        self.line(x, y, x + self.cell_size, y, t) # down horizontal line (down)
        
    def draw_right(self,x, y, t):
        self.line(x + self.cell_size, y, x + self.cell_size, y + self.cell_size, t) # right vertical line (right)

    def draw_left(self,x, y, t):
        self.line(x, y, x, y + self.cell_size, t) # left vertical Line (left)



    def update_maze_explored(self,visited_cell,maze_map,t):
        visited_cell = (6-visited_cell[0],visited_cell[1])
        self.draw_point(visited_cell,t)
    
        x = (visited_cell[1] + 1) * self.cell_size + self.start_x - self.cell_size
        y = (visited_cell[0] + 1) * self.cell_size + self.start_y - self.cell_size

        self.draw_wall(maze_map.grid[visited_cell[0]][visited_cell[1]],x, y, t)

    # initlize a sudo map

    def draw_point(self,visited_cell,t):
        
        CIRCLE_SIZE = 6
        y = (visited_cell[0] + 1) * self.cell_size + self.start_y - CIRCLE_SIZE - self.cell_size//2
        x = (visited_cell[1] + 1) * self.cell_size + self.start_x - self.cell_size//2

        t.penup()
        t.goto(x, y) #last position
        t.pendown()
        t.fillcolor("black")
        t.begin_fill()
        t.circle(CIRCLE_SIZE)
        t.end_fill()
        t.penup()

    
def init_map():
     
    maze_map = Grid(ROWS, COLUMNS)
    # Initialize the grid with cells
    for row in range(ROWS):
        for col in range(COLUMNS):
            maze_map.add_cell(row, col, Cell(True, True, True, True))
    return maze_map


def main():
    maze_view = MazeView()
    maze_map = init_map()
    text, maze = maze_view.init_maze(maze_map)
    

    
    done()

main()
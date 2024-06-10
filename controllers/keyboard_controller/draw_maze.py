from turtle import *
# import var
from constants import *




class MazeView:
    def __init__(self,cell_size = 60) -> None:
        self.BORDERS = 100
        self.cell_size = cell_size
        self.WIDTH = self.BORDERS + cell_size * COLUMNS
        self.HEIGHT = self.BORDERS + cell_size * ROWS
        self.start_y , self.start_x = -(self.HEIGHT-self.BORDERS) // 2 , -(self.WIDTH-self.BORDERS) // 2 
        self.end_y   , self.end_x   = (self.HEIGHT-self.BORDERS) // 2 , (self.WIDTH-self.BORDERS) // 2 
        
        self.maze_drawer = Turtle()
        self.maze_drawer.hideturtle()
        tracer(False)
        self.maze_drawer.color('black')
        self.maze_drawer.width(1)
        
        self.grid_drawer = Turtle()
        self.grid_drawer.hideturtle()
        self.grid_drawer.color('black')
        self.grid_drawer.width(1)

    def init_maze(self,maze_map):
        
        setup(self.WIDTH, self.HEIGHT,800) #size and position on screen


        #draw grid
        
        for y in range(self.start_y, self.end_y, self.cell_size):
            for x in range(self.start_x, self.end_x, self.cell_size):
                self.line(x, y + self.cell_size, x + self.cell_size, y + self.cell_size)
                self.line(x + self.cell_size, y, x + self.cell_size, y + self.cell_size)
                self.line(x, y, x + self.cell_size, y)
                self.line(x, y, x, y + self.cell_size)

        #draw walls
        i = 0
        j = 0
        for y in range(self.start_y, self.end_y, self.cell_size):
            i = 0
            for x in range(self.start_x, self.end_x, self.cell_size):
                self.draw_wall(maze_map.grid[j][i], x, y)
                i+=1
            j+=1


    def line(self,start_x, start_y, end_x, end_y,draw_border = False):
        if(draw_border):
            self.grid_drawer.width(5)
        self.grid_drawer.up()
        self.grid_drawer.goto(start_x, start_y)
        self.grid_drawer.down()
        self.grid_drawer.goto(end_x, end_y) 
        self.grid_drawer.up()
        self.grid_drawer.goto(start_x, start_y)
        self.grid_drawer.down()
        self.grid_drawer.goto(end_x, end_y)
        self.grid_drawer.width(1) 
        


    def draw_wall(self,cell, x, y):
        if cell is None:
            return
        
        
        if not cell.visited:
            return
                
        if cell.up_wall:
            self.draw_top(x, y)
        if cell.down_wall:
            self.draw_bottom(x, y)
        if cell.right_wall:
            self.draw_right(x, y)
        if cell.left_wall:
            self.draw_left(x, y)
        

    def draw_top(self,x, y):
        self.line(x, y + self.cell_size, x + self.cell_size, y + self.cell_size,True) # up horizontal line (top)

    def draw_bottom(self,x, y):
        self.line(x, y, x + self.cell_size, y,True) # down horizontal line (down)
        
    def draw_right(self,x, y):
        self.line(x + self.cell_size, y, x + self.cell_size, y + self.cell_size,True) # right vertical line (right)

    def draw_left(self,x, y):
        self.line(x, y, x, y + self.cell_size,True) # left vertical Line (left)



    def update_maze_explored(self,visited_cell,maze_map):
        fixed_pos = (6-visited_cell[0],visited_cell[1])
        self.draw_point(fixed_pos)
        x = (fixed_pos[1] + 1) * self.cell_size + self.start_x - self.cell_size
        y = (fixed_pos[0] + 1) * self.cell_size + self.start_y - self.cell_size

        self.draw_wall(maze_map.grid[visited_cell[0]][visited_cell[1]],x, y)
        update()

    # initlize a sudo map

    def draw_point(self,visited_cell):
        
        CIRCLE_SIZE = 10
        y = (visited_cell[0] + 1) * self.cell_size + self.start_y - self.cell_size//2
        x = (visited_cell[1] + 1) * self.cell_size + self.start_x - self.cell_size//2

        self.maze_drawer.up()
        self.maze_drawer.goto(x, y)
        self.maze_drawer.dot(CIRCLE_SIZE,'red')
        self.maze_drawer.down()
    
    def done(self):
        done()



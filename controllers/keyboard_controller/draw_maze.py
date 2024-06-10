from turtle import *
import var
from constants import *

def init_maze(maze_map,cell_size):
    setup(1020, 1020, 1500, 160) #size and position on screen
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
    for y in range(-480, 480, cell_size):
        for x in range(-480, 480, cell_size):
            line(x, y + cell_size, x + cell_size, y + cell_size, grid)
            line(x + cell_size, y, x + cell_size, y + cell_size, grid)
            line(x, y, x + cell_size, y, grid)
            line(x, y, x, y + cell_size, grid)

    maze.width(5)
    #draw walls
    i = 0
    
    for y in range(-480, 480, cell_size):
        for x in range(-480, 480, cell_size):
            cell = graph_walls_convert(maze_map[i], i)
            draw_wall(cell, x, y, cell_size, maze)
            i += 1

    return text, maze

def line(start_x, start_y, end_x, end_y, t):
    t.up()
    t.goto(start_x, start_y)
    t.down()
    t.goto(end_x, end_y) 


def draw_wall(maze_map, x, y, size, t):
    line(x, y + size, x + size, y + size, t) # up horizontal line (top)
    line(x + size, y, x + size, y + size, t) # right vertical line (right)
    line(x, y, x + size, y, t) # down horizontal line (down)
    line(x, y, x, y + size, t) # left vertical Line (left)

    if maze_map.grid[x][y]
    
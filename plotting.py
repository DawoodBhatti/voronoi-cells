import turtle as tur
import colorsys as cs
from random import randint, random

#draw multiple cells simultaneously using the turtle package
#threading turtle drawing to approximate simultaneous drawing

tur.TurtleScreen._RUNNING = True
tur.setup(width = 0.5, height = 0.5, startx = 10, starty = 10)
tur.resetscreen()  # Clears everything and resets the state


#draws a cell given at least 2 vertices (x,y)
def draw_single_cell(vertices = [(10,10), (17, -15), (55, 28)]):


    tur.speed(0)
    tur.width(2)
    tur.bgcolor("gray")
    tur.color("white")
    
    # move to each vertex, drawing from the first onwards
    tur.teleport(vertices[0][0], vertices[0][1])
    for v in vertices:        
        tur.goto(v[0], v[1])
    tur.goto(vertices[0][0], vertices[0][1])

    print("i'm done drawing now")
    print("starting to build this real cool function")
    

def draw_multicells(num_cells = 5):
    all_vertices = create_vertices(num_cells) 
    
    for vertices in all_vertices:
        draw_single_cell(vertices)
    
    print("starting to build this real cool function")


def draw_multicell_simultaneously(num_cells = 5):
    all_vertices = create_vertices(num_cells) 
    
    for vertices in all_vertices:
        draw_single_cell(vertices)
    
    print("starting to build this real cool function")


def create_vertices(num_cells = 5):
    vertices = []
    
    for cells in range(num_cells):
        tuple_coords = []
        
        for points in range(randint(3,5)):
            tuple_coords.append((randint(-300,300), randint(-300,300)))
        
        vertices.append(tuple_coords)
    
    return vertices

draw_multicell_simultaneously()
tur.done()
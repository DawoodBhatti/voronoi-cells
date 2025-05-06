import queue
import threading
import turtle
import math
import random
from voronoi_cells import generate_voronoi_cells

#TODO: add voronoi levels to this, e.g. remove some points and replot with different filters, colours, etc
#TODO: mess around with fitting ellipsoids to shapes?
#TODO: try creating a shading profile
#TODO: translate to gdscript

# Global variables for screen size
turtle.TurtleScreen._RUNNING = True

WINDOW_WIDTH = turtle.window_width()
WINDOW_HEIGHT = turtle.window_height()

WIDTH = 0.9
HEIGHT = 0.9

X_RANGE = WINDOW_WIDTH * WIDTH  
Y_RANGE = WINDOW_HEIGHT * HEIGHT  

class TurtleDrawing:
    def __init__(self, name, vertices):
        """Immediately draw a Voronoi cell upon turtle creation."""
        self.vertices = vertices
        self.turtle_object = turtle.Turtle()
        self.turtle_object.hideturtle()  # Keep turtle hidden

        self.turtle_object.speed("fastest")
        self.turtle_object.width(2)
        self.turtle_object.color("black")

        self.draw_cell()

    def draw_cell(self):
        """Draw the entire Voronoi cell instantly upon initialization."""
        self.turtle_object.penup()
        self.turtle_object.goto(self.vertices[0])
        self.turtle_object.pendown()

        for x, y in self.vertices:
            self.turtle_object.goto(x, y)

        self.turtle_object.goto(self.vertices[0])  # Close the shape

def draw_shapes(shape_vertices):
    """Spawn and instantly draw each Voronoi cell."""
    for i, vertices in enumerate(shape_vertices):
        graphics.put(lambda v=vertices: TurtleDrawing("turt" + str(i), v))

def process_queue():
    """Process the function queue for execution."""
    while not graphics.empty():
        (graphics.get())()

    turtle.ontimer(process_queue, 100)

def plot_voronoi(shape_vertices, seed_points=None, show_seed_points=True, show_voronoi=True):
    """Unified function to visualize seed points and Voronoi cells."""
    turtle.TurtleScreen._RUNNING = True
    turtle.resetscreen()
    turtle.setup(width=0.9, height=0.9)

    if show_seed_points and seed_points:
        seed_turtle = turtle.Turtle()
        seed_turtle.hideturtle()
        seed_turtle.speed("fastest")
        seed_turtle.color("blue")

        for x, y in seed_points:
            seed_turtle.penup()
            seed_turtle.goto(x, y)
            seed_turtle.pendown()
            seed_turtle.dot(5)

    if show_voronoi:
        global graphics
        graphics = queue.Queue(3)

        thread1 = threading.Thread(target=draw_shapes, args=(shape_vertices,))
        thread1.daemon = True
        thread1.start()

        process_queue()

    turtle.done()
    print("Plotting complete!")

# Generate Voronoi cells and plot
voronoi_data, seed_points = generate_voronoi_cells(x_range=X_RANGE, y_range=Y_RANGE, 
                                                   num_points=120, 
                                                   offset_x=-X_RANGE/2, offset_y=-Y_RANGE/2, 
                                                   distribution_method="random")

plot_voronoi(voronoi_data, seed_points, show_seed_points=True, show_voronoi=True)

#distributions available:
        #"halton"
        #"fibonacci"
        #"poisson"
        #"random"


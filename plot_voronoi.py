import queue
import threading
import turtle
import math
import random
from voronoi_cells import generate_voronoi_cells

#receive cell vertices from voronoi_cells.py
#draw multiple cells/shapes almost simultaneously

#TODO: fix dists and get colour in with triangles maybe?
#TODO: structre program to use different distributions: random, Halton Sequence, fib sequence
#TODO: add some colouring into this
#TODO: add voronoi levels to this, e.g. remove some points and replot with different filters, colours, etc
#TODO: mess around with fitting ellipsoids to shapes?
#TODO: try creating a shading profile
#TODO: translate to gdscript


turtle.TurtleScreen._RUNNING = True

# Global variables for screen size
WINDOW_WIDTH = turtle.window_width()
WINDOW_HEIGHT = turtle.window_height()

# Display fractions
WIDTH = 0.9
HEIGHT = 0.9

# Calculate x_range and y_range based on screen size
X_RANGE = WINDOW_WIDTH * WIDTH  # Keep it within 80% of the screen
Y_RANGE = WINDOW_HEIGHT * HEIGHT

class TurtleDrawing:
    def __init__(self, name=None, vertices=None):
        if vertices is None:
            self.vertices = [(-100, 10), (117, -15), (55, 28)]  # Default empty coordinates
        else:
            self.vertices = vertices

        #set turtle up at first point of shape
        self.turtle_object = turtle.Turtle()
        self.turtle_name = name
                
        # Hide turtle before setting position
        self.turtle_object.hideturtle()
        self.turtle_object.teleport(self.vertices[0][0], self.vertices[0][1])
        self.turtle_object.showturtle()
        self.turtle_object.speed("fastest")
        self.turtle_object.width(2)
        self.turtle_object.color("black")
        self.vertex_counter = 1
        self.completed = False


    def draw_next_point(self):
        """Move turtle to the next vertex, closing the shape after the last point."""
        if self.vertex_counter < len(self.vertices):
            x, y = self.vertices[self.vertex_counter]

            #movement and logging inside the same lambda
            graphics.put(lambda x=x, y=y: (self.turtle_object.goto(x, y), print(self.turtle_name, " moved to:", x, ", ", y)))
            self.vertex_counter += 1

        elif self.vertex_counter == len(self.vertices):
            x, y = self.vertices[0]

            #close the loop with a final movement and statement together
            graphics.put(lambda x=x, y=y: (self.turtle_object.goto(x, y), print(self.turtle_name, " is closing the loop at:", x, ", ", y)))

            self.vertex_counter += 1
            self.completed = True

            self.turtle_object.hideturtle()

        else:
            print(self.turtle_name, " is loafing about")
            

def draw_shapes(number_of_shapes, shape_vertices, max_points):
    """Create turtle objects and queue their drawing functions"""
    #create objects
    turtles = []
    for i in range(number_of_shapes):
        turtles.append(TurtleDrawing("turt" + str(i), shape_vertices[i]))

    #add draw_next_point to function call queue
    for mp in range(max_points + 1):
        for t in turtles:
            if not t.completed:
                graphics.put(lambda t=t: t.draw_next_point())


def process_queue():
    """Process the function queue for execution"""
    while not graphics.empty():
        (graphics.get())()  #call next queued function with optional arguments

    if threading.active_count() > 1:
        turtle.ontimer(process_queue, 100)
        
        
def plot_voronoi(shape_vertices, seed_points=None, show_seed_points=True, show_voronoi=True):
    """
    Unified function to visualize seed points and Voronoi cells.

    Parameters:
        shape_vertices (list): List of Voronoi cell vertex sets.
        seed_points (list, optional): List of seed points used for generation.
        show_seed_points (bool): If True, displays seed points.
        show_voronoi (bool): If True, displays Voronoi cells.
    """
    turtle.TurtleScreen._RUNNING = True
    turtle.resetscreen()
    turtle.setup(width=0.9, height=0.9)

    if show_seed_points and seed_points:
        seed_turtle = turtle.Turtle()
        seed_turtle.hideturtle()
        seed_turtle.speed("fastest")
        seed_turtle.color("blue")  # Seed points color

        for x, y in seed_points:
            seed_turtle.penup()
            seed_turtle.goto(x, y)
            seed_turtle.pendown()
            seed_turtle.dot(5)  # Draw small circles at seed points

    if show_voronoi:
        number_of_shapes = len(shape_vertices)
        max_points = max(len(i) for i in shape_vertices)

        global graphics
        graphics = queue.Queue(3)

        thread1 = threading.Thread(target=draw_shapes, args=(number_of_shapes, shape_vertices, max_points))
        thread1.daemon = True
        thread1.start()

        process_queue()

    turtle.done()
    print("Plotting complete!")


#run code
voronoi_data, seed_points = generate_voronoi_cells(x_range=X_RANGE, y_range=Y_RANGE, 
                                                   num_points=120, 
                                                   offset_x=-X_RANGE/2, offset_y=-Y_RANGE/2, 
                                                   distribution_method="random")
#visualize_seed_points(seed_points)
plot_voronoi(voronoi_data, seed_points, show_seed_points=True, show_voronoi=True)

#distributions available:
        #"halton"
        #"fibonacci"
        #"poisson"
        #"random"
    
import queue
import threading
import turtle
import math
import random
from voronoi_cells import generate_voronoi_cells

#receive cell vertices from voronoi_cells.py
#draw multiple cells/shapes almost simultaneously


#TODO: add some colouring into this
#TODO: add voronoi levels to this, e.g. remove some points and replot with different filters, colours, etc
#TODO: mess around with fitting ellipsoids to shapes?
#TODO: try creating a shading profile
#TODO: translate to gdscript

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


def run(shape_vertices):
    """main execution function to set up, run threads, and process queue"""
    
    #close existing windows and set up
    turtle.TurtleScreen._RUNNING = True
    turtle.resetscreen()  # Clears everything and resets the state
    turtle.setup(width=0.9, height=0.9, startx=0, starty=0)
    
    number_of_shapes = len(shape_vertices)
    max_points = 0

    for i in shape_vertices:
        if len(i) > max_points:
            max_points = len(i)
    
    #set up graphics queue 
    global graphics
    graphics = queue.Queue(3)  #size of function queue
    
    thread1 = threading.Thread(target=draw_shapes, args=(number_of_shapes, shape_vertices, max_points))
    thread1.daemon = True  #thread dies when main thread exits
    thread1.start()

    #begin queue processing
    process_queue()

    turtle.done()
    print("all done son!")


#run code
voronoi_data, seed_points = generate_voronoi_cells(x_range=1000, y_range=500, num_points=50, offset_x=-500, offset_y=-250)

run(voronoi_data)
import queue
import threading
import turtle
import math
import random
import colorsys as cs
from random import randint


#close existing windows and set up
turtle.TurtleScreen._RUNNING = True
turtle.resetscreen()  # Clears everything and resets the state
turtle.setup(width=0.9, height=0.9, startx=0, starty=0)

#global list of turtle objects
turtles = []

class TurtleDrawing:
    def __init__(self, name=None, vertices=None):
        if vertices is None:
            self.vertices = [(-100, 10), (117, -15), (55, 28)]  #default empty coordinates
        else:
            self.vertices = vertices

        #set turtle up at first point of shape
        self.turtle_object = turtle.Turtle()
        self.turtle_name = name
        self.turtle_object.teleport(self.vertices[0][0], self.vertices[0][1])
        self.turtle_object.speed("fastest")
        self.turtle_object.width(2)
        self.turtle_object.color("black")
        self.vertex_counter = 0
        self.completed = False


    def draw_next_point(self):
        """Move turtle to the next vertex, closing the shape after the last point"""
        if self.vertex_counter < len(self.vertices):
            x, y = self.vertices[self.vertex_counter]

            #movement and logging inside the same lambda
            graphics.put(lambda x=x, y=y: (self.turtle_object.goto(x, y), print(self.turtle_name, " moved to:", x, ", ", y)))
            self.vertex_counter += 1

        elif self.vertex_counter == len(self.vertices):
            x, y = self.vertices[0]

            #close the loop with a final movement and print statement together
            graphics.put(lambda x=x, y=y: (self.turtle_object.goto(x, y), print(self.turtle_name, " is closing the loop at:", x, ", ", y)))

            self.vertex_counter += 1
            self.completed = True

            self.turtle_object.hideturtle()

        else:
            print(self.turtle_name, " is loafing about")
        
            
def generate_tessellated_hexagons(size=35):
    """Generate a perfectly tessellated hexagonal grid starting from the bottom-left"""
    
    hexagons = []

    #get screen size dynamically
    screen_width = turtle.window_width()
    screen_height = turtle.window_height()

    h_spacing = 2 * size * math.cos(math.radians(30)) # Correct hex width spacing
    v_spacing = 1.5 * size  # Correct hex height spacing

    #compute max rows & cols based on the screen size
    cols = math.ceil(screen_width / (v_spacing)) + 3 #horizontal hexagon spacing
    rows = math.ceil(screen_height / (h_spacing)) + 1 #vertical hexagon spacing

    #adjust starting position to **bottom-left** of the screen
    start_x = -screen_width / 2 + size  #shift left to start at bottom
    start_y = -screen_height / 2 + size  #shift down to start at bottom

    for row in range(rows):
        for col in range(cols):
            #offset odd rows for staggered tiling
            x_offset = start_x + col * h_spacing
            if row % 2 == 1:
                x_offset += h_spacing / 2
            
            y_offset = start_y + row * v_spacing

            hexagons.append(generate_hexagon(x_offset, y_offset, size))
    
    return hexagons


def generate_hexagon(cx, cy, radius):
    """Generate hexagon vertices centered at (cx, cy) with given radius"""
    return [
        (cx, cy + radius),
        (cx + radius * 0.87, cy + radius * 0.5),
        (cx + radius * 0.87, cy - radius * 0.5),
        (cx, cy - radius),
        (cx - radius * 0.87, cy - radius * 0.5),
        (cx - radius * 0.87, cy + radius * 0.5)
    ]


def paint_hexagons():
    """Paint all of the generated hexagons because style?"""
    for t in turtles:
        print("painting: ", t.turtle_name)
        #normalise hsv values by dividing values here https://www.selecolor.com/en/hsv-color-picker/ by 360, 100 and 100
        t.turtle_object.color(cs.hsv_to_rgb(60/360, 80/100, randint(60, 100)/100))


def draw_shapes(number_of_shapes, shape_vertices, max_points):
    """Create turtle objects, queue their drawing functions and color when done!"""
    #create turtle objects
    global turtles
    for i in range(number_of_shapes):
        turtles.append(TurtleDrawing("turt" + str(i), shape_vertices[i]))

    graphics.put(lambda: paint_hexagons())
    
    #add draw_next_point to function call queue
    for mp in range(max_points + 1):
        for t in turtles:
            if not t.completed:
                graphics.put(lambda t=t: t.draw_next_point())


def process_queue():
    """Process the function queue for execution"""
    while not graphics.empty():
        (graphics.get())()  #call the next queued function

    if threading.active_count() > 1:
        turtle.ontimer(process_queue, 100)


def run():
    """Main execution function to set up, run threads, and process queue"""
    #generate hexagon vertices
    shape_vertices = generate_tessellated_hexagons()
    shape_vertices.sort(key=lambda hex: hex[0][1])  #sort by y-position (first vertex in each hexagon)
    random.shuffle(shape_vertices)
    number_of_shapes = len(shape_vertices)
    max_points = 0

    for i in shape_vertices:
        if len(i) > max_points:
            max_points = len(i)

    global graphics
    graphics = queue.Queue(3)  #size of function queue

    thread1 = threading.Thread(target=draw_shapes, args=(number_of_shapes, shape_vertices, max_points))
    thread1.daemon = True  #thread dies when main thread exits
    thread1.start()

    process_queue()

    turtle.done()
    print("all done son!")


#run the main function
run()

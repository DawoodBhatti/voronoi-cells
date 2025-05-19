import queue
import threading
import turtle
import time
from voronoi_cells import generate_voronoi_cells
from voronoi_to_delauney import generate_quadrants, run_delauney

class TurtleDrawing:
    def __init__(self, name, vertices, line_width=5, line_colour="black", spawn_draw=False):
        """Create a turtle object to draw given vertices with customizable width."""
        self.name = name
        self.vertices = vertices
        self.turtle_object = turtle.Turtle()
        self.turtle_object.hideturtle()
        self.turtle_object.speed("fastest")
        self.turtle_object.width(line_width)  # Set line width
        self.turtle_object.color(line_colour) # Set line colour
        
        if spawn_draw:        
            self.draw_cell()


    def draw_cell(self):
        """Draw the cell defined by vertices."""
        self.turtle_object.penup()
        self.turtle_object.goto(self.vertices[0])
        self.turtle_object.pendown()

        for x, y in self.vertices:
            self.turtle_object.goto(x, y)

        self.turtle_object.goto(self.vertices[0])  # Close the shape

        
def compute_square_vertices(quadrant):
    """Compute the four vertex points of a square centered at the quadrant's midpoint."""
    x, y = quadrant.midpoint
    size = quadrant.length / 2  # Half-length to calculate offsets

    return [
        (x - size, y - size),  # Bottom-left
        (x + size, y - size),  # Bottom-right
        (x + size, y + size),  # Top-right
        (x - size, y + size)   # Top-left
    ]


def draw_delauney_cells(shape_vertices):
    """Queue Delauney cell drawing operations."""
    for i, vertices in enumerate(shape_vertices):
        graphics.put(lambda v=vertices, idx=i: TurtleDrawing("delauney_" + str(idx), v, 1, "green", True))


def draw_voronoi_cells(shape_vertices):
    """Queue Voronoi cell drawing operations."""
    for i, vertices in enumerate(shape_vertices):
        graphics.put(lambda v=vertices, idx=i: TurtleDrawing("voronoi_" + str(idx), v, 5, "black", True))
        

def draw_single_seed_point(x, y, name=None):
    """Draw an individual seed point using global (invisible) seed turtle."""
    seed_turtle.penup()
    seed_turtle.goto(x, y)
    seed_turtle.pendown()
    seed_turtle.dot(5)

    # if name is not None:
    #     seed_turtle.penup()
    #     seed_turtle.write(name, align="center", font=("Arial", 12, "bold"))
    #     seed_turtle.pendown()


def draw_quadrants(quadrants):
    """Queue quadrant square drawing operations with thinner lines."""
    quadrants_list = quadrants.flatten().tolist() # Convert to standard Python list

    for i, quadrant in enumerate(quadrants_list):
        square_vertices = compute_square_vertices(quadrant)
        graphics.put(lambda i=i, v=square_vertices: TurtleDrawing("quadrant_" + str(i), v, 1, "red", True))  # Set width to 1


def process_queue():
    """Process queued drawing functions."""
    while not graphics.empty():
        task = graphics.get()
        task()
        time.sleep(0.01)  # Small delay to ensure ordered execution

    turtle.ontimer(process_queue, 50)


def plot_voronoi(shape_vertices):
    """Start Voronoi cell plotting."""
    thread = threading.Thread(target=draw_voronoi_cells, args=(shape_vertices,))
    thread.daemon = True
    thread.start()


def plot_delauney(shape_vertices):
    """Start Voronoi cell plotting."""
    thread = threading.Thread(target=draw_delauney_cells, args=(shape_vertices,))
    thread.daemon = True
    thread.start()


def plot_seed_points(seed_points):
    """Queue seed points for threaded drawing."""
    for i, (x, y) in enumerate(seed_points):
        graphics.put(lambda x=x, y=y, i=i: draw_single_seed_point(x, y, name=i))


def plot_quadrants(quadrants):
    """Start quadrant plotting"""
    thread = threading.Thread(target=draw_quadrants, args=(quadrants,))
    thread.daemon = True
    thread.start()


def initialize_turtle_screen():
    """Initialize the Turtle screen settings."""
    global seed_turtle
    turtle.TurtleScreen._RUNNING = True
    turtle.resetscreen()
    turtle.setup(width=0.9, height=0.9)

    # Create a single hidden turtle for seed points
    seed_turtle = turtle.Turtle()
    seed_turtle.hideturtle()
    seed_turtle.speed("fastest")
    seed_turtle.color("blue")
    
    
def initialize_graphics_queue():
    """Initialize the global graphics queue once."""
    global graphics
    graphics = queue.Queue()


def compute_window_size():
    """Compute and set global window size variables."""
    global WINDOW_WIDTH, WINDOW_HEIGHT, WIDTH, HEIGHT, X_RANGE, Y_RANGE
    WINDOW_WIDTH = turtle.window_width()
    WINDOW_HEIGHT = turtle.window_height()
    WIDTH, HEIGHT = 0.9, 0.9
    X_RANGE, Y_RANGE = WINDOW_WIDTH * WIDTH, WINDOW_HEIGHT * HEIGHT


def generate_data():
    """Generate Voronoi cells, seed points, and quadrants."""
    try:
        voronoi_data, seed_points = generate_voronoi_cells(
            x_range=X_RANGE, y_range=Y_RANGE, num_points=4800, 
            offset_x=-X_RANGE/2, offset_y=-Y_RANGE/2, distribution_method="fibonacci_segments"
        )
        # Choose a distribution method
        #"halton":
        #"fibonacci"
        #"fibonacci_segments"
        #"poisson"
        #"random"
        
        quadrants, delauney_triangles = run_delauney(voronoi_data, seed_points)
        return voronoi_data, seed_points, quadrants, delauney_triangles
    except Exception as e:
        print(f"Error generating data: {e}")
        return [], [], []


def plot_graphics(voronoi_data, seed_points, quadrants, delauney_triangles):
    """Plot seed points, Voronoi cells, and quadrants."""
    plot_seed_points(seed_points)
    #plot_voronoi(voronoi_data)
    #plot_quadrants(quadrants)
    plot_delauney(delauney_triangles)


def main():
    """Main function to initialize everything and start plotting."""
    initialize_turtle_screen()
    initialize_graphics_queue()
    compute_window_size()

    # Generate Data
    voronoi_data, seed_points, quadrants, delauney_triangles = generate_data()

    # Start plots
    plot_graphics(voronoi_data, seed_points, quadrants, delauney_triangles)

    # Start queue processing
    process_queue()

    # Keep the turtle window open
    turtle.done()
    print("Plotting complete!")

# Run main function when script is executed
if __name__ == "__main__":
    main()

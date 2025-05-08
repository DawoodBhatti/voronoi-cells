import queue
import threading
import turtle
from voronoi_cells import generate_voronoi_cells
from voronoi_to_delauney import generate_quadrants

class TurtleDrawing:
    def __init__(self, name, vertices, spawn_draw=False):
        """Create a turtle object to draw given vertices."""
        self.vertices = vertices
        self.turtle_object = turtle.Turtle()
        self.turtle_object.hideturtle()  # Keep turtle hidden
        self.turtle_object.speed("fastest")
        self.turtle_object.width(2)
        self.turtle_object.color("black")
        
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

def draw_voronoi_cells(shape_vertices):
    """Queue Voronoi cell drawing operations."""
    for i, vertices in enumerate(shape_vertices):
        graphics.put(lambda v=vertices: TurtleDrawing("voronoi_" + str(i), v, True))

def draw_seed_points(seed_points):
    """Queue seed points for threaded drawing."""
    for x, y in seed_points:
        graphics.put(lambda x=x, y=y: draw_single_seed_point(x, y))

def draw_single_seed_point(x, y):
    """Draw an individual seed point."""
    seed_turtle = turtle.Turtle()
    seed_turtle.hideturtle()
    seed_turtle.speed("fastest")
    seed_turtle.color("blue")
    
    seed_turtle.penup()
    seed_turtle.goto(x, y)
    seed_turtle.pendown()
    seed_turtle.dot(5)

def draw_quadrants(quadrants):
    """Queue quadrant drawing operations."""
    for i, vertices in enumerate(quadrants):
        graphics.put(lambda v=vertices: TurtleDrawing("quadrant_" + str(i), v, True))

def process_queue():
    """Process queued drawing functions."""
    while not graphics.empty():
        (graphics.get())()

    turtle.ontimer(process_queue, 100)

def plot_voronoi(shape_vertices):
    """Start Voronoi cell plotting."""
    global graphics
    graphics = queue.Queue()

    thread = threading.Thread(target=draw_voronoi_cells, args=(shape_vertices,))
    thread.daemon = True
    thread.start()

def plot_seed_points(seed_points):
    """Queue seed points for threaded drawing."""
    for x, y in seed_points:
        graphics.put(lambda x=x, y=y: draw_single_seed_point(x, y))

    process_queue()

def plot_quadrants(quadrants):
    """Start quadrant plotting."""
    global graphics
    graphics = queue.Queue()

    thread = threading.Thread(target=draw_quadrants, args=(quadrants,))
    thread.daemon = True
    thread.start()

def initialize_turtle_screen():
    """Initialize the Turtle screen settings."""
    turtle.TurtleScreen._RUNNING = True
    turtle.resetscreen()
    turtle.setup(width=0.9, height=0.9)
    turtle.hideturtle()  # Hide the default turtle
    
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
            x_range=X_RANGE, y_range=Y_RANGE, num_points=15, 
            offset_x=-X_RANGE/2, offset_y=-Y_RANGE/2, distribution_method="fibonacci"
        )
        quadrants = generate_quadrants(voronoi_data)
        return voronoi_data, seed_points, quadrants
    except Exception as e:
        print(f"Error generating data: {e}")
        return [], [], []

def plot_graphics(voronoi_data, seed_points, quadrants):
    """Plot seed points, Voronoi cells, and quadrants."""
    plot_seed_points(seed_points)
    plot_voronoi(voronoi_data)
    # plot_quadrants(quadrants)

def main():
    """Main function to initialize everything and start plotting."""
    initialize_turtle_screen()
    initialize_graphics_queue()
    compute_window_size()

    # Generate Data
    voronoi_data, seed_points, quadrants = generate_data()

    # Start plots
    plot_graphics(voronoi_data, seed_points, quadrants)

    # Start queue processing
    process_queue()

    # Keep the turtle window open
    turtle.done()
    print("Plotting complete!")

# Run main function when script is executed
if __name__ == "__main__":
    main()

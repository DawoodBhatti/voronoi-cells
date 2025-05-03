import turtle as tur
import colorsys as cs

# basic demo of turtle
def draw_spiral():
    
    tur.setup(750, 750, 10, 10)
    tur.speed(0)
    tur.width(2)
    tur.bgcolor("black")
    
    for j in range(29):
      for i in range(15):
         tur.color(cs.hsv_to_rgb(i/15, j/29,1))
         tur.right(90)
         tur.circle(200-j*4,90)
         tur.left(90)
         tur.circle(200-j*4,90)
         tur.right(180)
         tur.circle(50,24)
         
    tur.hideturtle()
    
    print("turtle is doneee")
 
    
def geometric_spiral():
    
    for steps in range(50):
        for c in ('blue', 'red', 'green'):
            tur.color(c)
            tur.forward(steps)
            tur.right(30)    
    
    
def geometric_sun():
    tur.setup(600, 600, 10, 10)

    tur.speed("fastest")  # Optional: speeds up drawing
    # tur.penup()  # Lift pen to avoid drawing while repositioning
    # tur.goto(0, 0)  # Move turtle to center of the screen
    # tur.pendown()  # Put pen down to start drawing
    
    tur.color('red')
    tur.fillcolor('yellow')
    tur.begin_fill()
    while True:
        tur.forward(200)
        tur.left(170)
        if abs(tur.pos()) < 1:
            break
    tur.end_fill()


# draw polygon cell on screen
def draw_a_cell():
    
    v1 = (10,10)
    v2 = (17, -15)
    v3 = (55, 28)
    
    tur.setup(750, 500, 10, 10)
    tur.speed(0)
    tur.width(2)
    tur.bgcolor("gray")
    tur.color("white")
    
    # move to each vertex, drawing from the first onwards
    tur.teleport(v1[0], v1[1]) 
    tur.goto(v2[0], v2[1])
    tur.goto(v3[0], v3[1])
    tur.goto(v1[0], v1[1])
    
    
    print("i'm done drawing now")



tur.TurtleScreen._RUNNING = True
tur.setup(width = 0.5, height = 0.5, startx = 10, starty = 10)

draw_a_cell()

tur.done()
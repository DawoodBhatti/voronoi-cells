import queue
import threading
import turtle
from time import sleep
from math import pi

turtle.setup(width = 0.5, height = 0.5, startx = 10, starty = 10)
turtle.resetscreen()  # Clears everything and resets the state


def tes1():
    for _ in range(360):
        graphics.put(lambda: turtle1.forward(10))
        graphics.put(lambda: turtle1.left(10))


def tes2():
    for _ in range(360):
        graphics.put(lambda: turtle2.forward(10))
        graphics.put(lambda: turtle2.right(10))

        
def tes3():
    graphics.put(lambda: turtle3.teleport(180/pi, 180/pi))
    for _ in range(360):
        graphics.put(lambda: turtle3.forward(10))
        graphics.put(lambda: turtle3.right(10))
        
def tes4():
    graphics.put(lambda: turtle4.teleport(-180/pi, 180/pi))
    for _ in range(360):
        graphics.put(lambda: turtle4.forward(10))
        graphics.put(lambda: turtle4.right(10))
        
        
def process_queue():
    while not graphics.empty():
        (graphics.get())()   # call the next queued function and pass an argument
        
    if threading.active_count() > 1:
        turtle.ontimer(process_queue, 100)


graphics = queue.Queue(3)  # size of function queue = number of hardware threads you have - 1. 
                           # maximum for my system appears to be 4: print(os.cpu_count())

turtle1 = turtle.Turtle()
turtle1.speed('fastest')
thread1 = threading.Thread(target=tes1)
thread1.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
thread1.start()

turtle2 = turtle.Turtle()
turtle2.speed('fastest')
thread2 = threading.Thread(target=tes2)
thread2.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
thread2.start()

turtle3 = turtle.Turtle()
turtle3.speed('fastest')
thread3 = threading.Thread(target=tes3)
thread3.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
thread3.start()

turtle4 = turtle.Turtle()
turtle4.speed('fastest')
thread4 = threading.Thread(target=tes4)
thread4.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
thread4.start()

process_queue()
turtle.done()
turtle.exitonclick()
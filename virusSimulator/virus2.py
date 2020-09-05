# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 13:38:20 2020

Ha, just had a great bug.   Nothing was turning green after 10 seconds.  
Turns out, the red would get reinfected and reset his timeInfected 
back to zero on each collision, while already red.  
So, I turned the elapsed time down to 3, and some circles would heal to green.

Another bug was is that once green, there is no immunity yet, 
so green turns back to red when it hits another red.

https://imgur.com/a/9juUkQN
https://pastebin.com/9Wh9X5nn
"""


from tkinter import *
import random
import time
import sys

# Constants
HEIGHT = 700
WIDTH = 900
TIME_TO_HEAL = 8
SPEED = 10
BALL_SIZE = 10
NUM_BALLS = 100
COLOR_START = 'blue'
COLOR_INFECTED = 'red'
COLOR_HEALED = 'green'

class Ball:
    
    # New BALL gnerates a random x,y location for the ball
    # The internal canvas graphics variable is NAMED shape
    # Also, init the x and y move increment (speed) as dx & dy
    def __init__(self, color, size):
        x1 = random.randrange(0,WIDTH)
        y1 = random.randrange(0,HEIGHT)
        self.shape = canvas.create_oval(x1, y1, x1+size, y1+size, fill=color)
        self.dx = random.randrange(-SPEED,SPEED)
        self.dy = random.randrange(-SPEED,SPEED)
        self.infectedTime = 0
        self.infected = False
        
    def checkHealed(self):
        if self.infected == True:
            totalTimeSick = time.time() - self.infectedTime

            if (totalTimeSick > TIME_TO_HEAL):
                canvas.itemconfig(self.shape, fill=COLOR_HEALED)
                self.infected = False
                self.infectedTime = 0
        
    def move(self):
        
        #Move the ball (shape variable in the ball instance
        canvas.move(self.shape, self.dx, self.dy)
        
        #get location of the ball
        pos = canvas.coords(self.shape)
        
        #Bounce off the edges of the window
        if pos[3] > HEIGHT or pos[1] < 0:
            self.dy = -self.dy
        if pos[0] < 0 or pos[2] > WIDTH:
            self. dx = -self.dx
        
        for b2 in balls:

            #ball can't hit itself, otherwise, you'll collide once in every loop
            if (balls.index(b2) == balls.index(self)):
                continue
            
            # Check if rectangles are overlapping
            # position = [x1,y1,x2,y2]
            # position = [LEFT, TOP, RIGHT, BOTTOM]
            pos2 = canvas.coords(b2.shape)
            if (pos[2] > pos2[0]) and (pos[0] < pos2[2]) and \
                (pos[3] > pos2[1]) and (pos[1] < pos2[3])                                                                                    :
                    self.dx = -self.dx
                    self.dy = -self.dy
                    
                    # I should really check that if EITHER is red,
                    # then they both become red.  Not just one direction.
                    # You can't get infected if HEALED or already SICK
                    # So, you can only get infected is color= START color
                    if (canvas.itemcget(self.shape,"fill") == COLOR_START):
                        if (canvas.itemcget(b2.shape,"fill") == COLOR_INFECTED):      
                            canvas.itemconfig(self.shape, fill=COLOR_INFECTED)
                            self.infected = True
                            self.infectedTime = time.time()

# Check if there are no more infected balls in the list
# Assume eradicated unless proved otherwise
def checkEradicated(balls):
    eradicated = True
    for b in balls:
        if (b.infected == True):
            eradicated = False
    return eradicated
                

# Initialize the drawing graphics canvas
tk = Tk()
canvas = Canvas(tk, width=WIDTH, height=HEIGHT)
tk.title("Virus!")
canvas.pack()   

timeStart = time.time()

# Declare a list of balls                                
balls = []

# Create balls and add to the list
for i in range(NUM_BALLS):
    b = Ball(COLOR_START, BALL_SIZE)
    balls.append(b)
    
# Make the first ball infected
canvas.itemconfig(balls[0].shape, fill=COLOR_INFECTED)
balls[0].infected = True
balls[0].infectedTime = time.time()

# Main loop to animate.  
# Iterate thru ball list
eradicated = False
while (eradicated == False):
    
    for ball in balls:
        ball.checkHealed()
        ball.move()
    tk.update() 
    #time.sleep(.05)  
    
    if (checkEradicated(balls) == True):
        elapsedTime = time.time() - timeStart
        print("Elapsed time to eradicate virus: {0}".format(elapsedTime))
        eradicated = True

# keeps main window open to prevent crash
# can gracefull close window manually
tk.mainloop()

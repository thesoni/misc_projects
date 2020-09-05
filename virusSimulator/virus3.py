# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 12:16:41 2020

@author: ssoni
"""

from tkinter import *
import random
import time

# Constants
HEIGHT = 400
WIDTH = 500
BALL_SIZE = 10
NUM_BALLS = 100
COLOR_START = "blue"
COLOR_INFECTED = "red"
COLOR_HEALED = "green"
SPEED = 10
TIME_TO_HEAL = 8

tk = Tk()
canvas = Canvas(tk, width=WIDTH, height=HEIGHT)
tk.title = "Virus Sim!"
canvas.pack()

class Ball:
    def __init__(self, color, size):
        x1 = random.randrange(0,WIDTH-size)    
        y1 = random.randrange(0,HEIGHT-size)    
        self.shape = canvas.create_oval(x1,y1,x1+size,y1+size, fill=color)
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
        #move ball
        canvas.move(self.shape,self.dx, self.dy)
        
        #get position
        pos = canvas.coords(self.shape)
        left = pos[0]
        top = pos[1]
        right = pos[2]
        bottom = pos[3]
                
        #check bounce
        if (right > WIDTH or left < 0):
            self.dx = -self.dx
            
        if (top < 0 or bottom > HEIGHT):
            self.dy = -self.dy

        #collision detection
        for b2 in balls:
            
            if (balls.index(b2) == balls.index(self)):
                continue
            
            pos2 = canvas.coords(b2.shape)            
            left2 = pos2[0]
            top2 = pos2[1]
            right2 = pos2[2]
            bottom2 = pos2[3]
            
            if (right > left2) and (left < right2) and \
                (bottom > top2) and (top < bottom2):
                    
                    #deflect both balls
                    self.dx = -self.dx
                    self.dy = -self.dy
                    b2.dx = -b2.dx
                    b2.dy = -b2.dy
                    
                    #get infected
                    #Check if the ball is blue (uninfected)
                    # and if the other ball is red (infected)
                    if (canvas.itemcget(self.shape, "fill") == COLOR_START):
                        if (canvas.itemcget(b2.shape, "fill") == COLOR_INFECTED):
                            canvas.itemconfig(self.shape, fill=COLOR_INFECTED)
                            self.infected = True
                            self.infectedTime = time.time()
            
def checkEradicated(balls):
    eradicated = True
    for b in balls:
        if (b.infected == True):
            eradicated = False
    return eradicated
                        
                    
balls = []

#Create balls
for i in range(NUM_BALLS):
        b = Ball(COLOR_START, BALL_SIZE)
        balls.append(b)

#Make one ball infected
canvas.itemconfig(balls[0].shape, fill=COLOR_INFECTED)
balls[0].infected=  True
balls[0].infectedTime = time.time()


while (checkEradicated(balls) == False):
    for ball in balls:
        ball.checkHealed()
        ball.move()
    tk.update()
    #time.sleep(.01)
    
   
tk.mainloop()


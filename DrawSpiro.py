import sys, random, argparse
import numpy as np
import math
import turtle
import random
from PIL import Image
from datetime import datetime
from fractions import gcd


#def drawCircleTurtle(x, y, r):
#    turtle.up()
#    turtle.setpos(x + r, y)
#    turtle.down()

#    for i in range(0, 365, 5):
#        a = math.radians(i)
#        turtle.setpos(x + r*math.cos(a), y + r*math.sin(a))
#drawCircleTurtle(0, 0, 50)
#turtle.mainloop()

class Spiro:
    def __init__(self, xc, yc, col, R, r, l):
        self.t = turtle.Turtle() #set the turtle object
        self.t.shape('turtle') #set the cursor shape
        self.step = 5
        self.drawingComplete = False

        self.setparams(xc, yc, col, R, r, l) #set params
        self.restart()

    def setparams(self, xc, yc, col, R, r, l):
        self.xc = xc
        self.yc = yc
        self.R = int(R)
        self.r = int(r)
        self.l = l
        self.col = col
        #reduce r/R to its smallest form using GCD
        gcdVal = gcd(self.r, self.R)
        self.nRot = self.r//gcdVal
        #get ratio of radii
        self.k = r/float(R)
        # set color
        self.t.color(*col)
        #store current angle
        self.a = 0

    def restart(self):
        self.drawingComplete = False
        self.t.showturtle()
        self.t.up()
        R, k, l = self.R, self.k, self.l
        a = 0.0
        x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
        y = R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
        self.t.setpos(self.xc + x, self.yc + y)
        self.t.down()

    def draw(self):
        R, k, l = self.R, self.k, self.l
        for i in range(0, 360*self.nRot + 1, self.step):
            a = math.radians(i)
            x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
            y = R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
            self.t.setpos(self.xc + x, self.yc + y)
            self.t.hideturtle()

    def update(self):
        if self.drawingComplete:
            return
        self.a += self.step
        R, k, l = self.R, self.k, self.l
        a = math.radians(self.a)
        x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
        y = R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
        self.t.setpos(self.xc + x, self.yc + y)
        if self.a >= 360*self.nRot:
            self.drawingComplete = True
            self.t.hideturtle()

    def clear(self):
        self.t.clear()

class SpiroAnimator:
    def __init__(self, N):
        self.deltaT = 10
        self.width = turtle.window_width()
        self.height = turtle.window_height()
        self.spiros = [] #create spiro object
        for i in range(N):
            rparams = self.genRandomParams() #gen random params
            spiro = Spiro(*rparams)
            self.spiros.append(spiro)
        turtle.ontimer(self.update, self.deltaT)

    def restart(self):
        for spiro in self.spiros:
            spiro.clear()
            rparams = self.genRandomParams()
            spiro.setparams(*rparams)
            spiro.restart()

    def genRandomParams(self):
        width, height = self.width, self.height
        R = random.randint(50, min(width, height)//2)
        r = random.randint(10, 9*R//10)
        l = random.uniform(0.1, 0.9)
        xc = random.randint(0, 0) #(-width//2, width//2)
        yc = random.randint(0, 0) #(-height//2, height//2)
        col = (random.random(), random.random(), random.random())
        return(xc, yc, col, R, r, l)

    def update(self):
        nComplete = 0
        for spiro in self.spiros:
            spiro.update()
            if spiro.drawingComplete:
                nComplete += 1
        if nComplete == len(self.spiros):
            self.restart()
        turtle.ontimer(self.update, self.deltaT)

    def toggleTurtles(self): # toggle turtle on and off
        for spiro in self.spiros:
            if spiro.t.isvisible():
                spiro.t.hideturtle()
            else:
                spiro.t.showturtle()

def main():
    print('generating spirograph')
    decStr = """This program draws Spirographs using the Turtle Module.
    When run with no arguments, this program draws random Spirographs.

    Terminology:
    R : radius of outer circle
    r : radius of inner circle
    l : ratio of hole distance to r
    """
    parser = argparse.ArgumentParser(description=decStr)

    parser.add_argument('--sparams', nargs=3, dest='sparams', required=False, help="The three arguments in sparams: R, r, l")
    args = parser.parse_args()

    turtle.setup(width=0.8)
    turtle.shape('turtle')

    turtle.title('Spirographs!')
    ######
    #start listening
    turtle.listen()
    turtle.hideturtle()

    if args.sparams:
        params = [float(x) for x in args.sparams]
        col = (0.0, 0.0, 0.0)
        spiro = Spiro(0, 0, col, *params)
        spiro.draw()
    else:
        spiroAnim = SpiroAnimator(1)
        turtle.onkey(spiroAnim.toggleTurtles, "t")
        turtle.onkey(spiroAnim.restart, "space")

    turtle.mainloop()

if __name__ == '__main__':
    main()

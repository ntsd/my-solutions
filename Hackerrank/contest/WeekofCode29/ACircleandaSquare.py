
#!/bin/python3

import sys

import numpy as np

import math

def circle_intersection(x1,y1,r1,x2,y2,r2):
        '''
        @summary: calculates intersection points of two circles
        @param circle1: tuple(x,y,radius)
        @param circle2: tuple(x,y,radius)
        @result: tuple of intersection points (which are (x,y) tuple)
        '''
        # return self.circle_intersection_sympy(circle1,circle2)
        #x1,y1,r1 = circle1
        #x2,y2,r2 = circle2
        # http://stackoverflow.com/a/3349134/798588
        dx,dy = x2-x1,y2-y1
        d = math.sqrt(dx*dx+dy*dy)
        if d > r1+r2:
##            print("#1")
            return None # no solutions, the circles are separate
        if d < abs(r1-r2):
##            print("#2")
            return None # no solutions because one circle is contained within the other
        if d == 0 and r1 == r2:
##            print("#3")
            return None # circles are coincident and there are an infinite number of solutions

        a = (r1*r1-r2*r2+d*d)/(2*d)
        h = math.sqrt(r1*r1-a*a)
        xm = x1 + a*dx/d
        ym = y1 + a*dy/d
        xs1 = xm + h*dy/d
        xs2 = xm - h*dy/d
        ys1 = ym - h*dx/d
        ys2 = ym + h*dx/d

        return xs1,ys1,xs2,ys2


def getDistance(x1, y1, x2, y2):
    dist = ( (x2 - x1)**2 + (y2 - y1)**2 )**0.5
    return dist

def is_between(ax, ay ,cx, cy ,bx, by):
    return getDistance(ax, ay, cx, cy) + getDistance(cx, cy, bx, by) == getDistance(ax, ay, bx, by)

w,h = input().strip().split(' ')
w,h = [int(w),int(h)]
circleX,circleY,r = input().strip().split(' ')
circleX,circleY,rCircle = [int(circleX),int(circleY),int(r)]
x1,y1,x3,y3 = input().strip().split(' ')
x1,y1,x3,y3 = [int(x1),int(y1),int(x3),int(y3)]
rectX, rectY = (x1+x3)/2, (y1+y3)/2
dameter = getDistance(x1, y1, x3, y3)
rRect = dameter/2
x2, y2, x4, y4 = circle_intersection(x1,y1,rRect,x3,y3,rRect)


print(rectX, rectY, rRect)
# your code goes here
for row in range(h):
    for col in range(w):
        #print(getDistance(c, r, circleX, circleY))
        if getDistance(col, row, circleX, circleY) <= rCircle:
            print("#",end="")
        #elif getDistance(col, row, rectX, rectY) <= (rRect-getDistance(col, row, rectX, rectY)):
        elif getDistance(col, row, rectX, rectY) < rRect or is_between(col, row ,x1,y1 ,x2, y2)\
             or is_between(col, row ,x1,y1 ,x4, y4) or is_between(col, row ,x3,y3 ,x2, y2) or is_between(col, row ,x3,y3 ,x4, y4):
            print("#",end="")
        else:
            print(".",end="")
    print()

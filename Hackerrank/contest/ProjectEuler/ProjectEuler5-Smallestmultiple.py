#!/bin/python3
import sys

def smallestMultiple(num):
    divideNumber = [i for i in range(num,num//2,-1)]
    n=1
    for i in range(2,num+1):
        n*=i
    l=num
    while 1:
        if all([n%i==0 for i in divideNumber]):
            while l>0:
                n2=n/l
##                print(n, l, file=sys.stderr)
                if all([n2%i==0 for i in divideNumber]):
                    n=n2
                    break
                l-=1
        if l<=1:
            return n*l

t = int(input().strip())
for a0 in range(t):
    n = int(input().strip())
    print(smallestMultiple(n))

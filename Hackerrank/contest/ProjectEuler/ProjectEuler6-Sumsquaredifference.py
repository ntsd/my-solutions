#!/bin/python3

def firstNum(num):
    return num*(num+1)*(num*2+1)//6

def secondNum(num):
    return (num*(num+1)//2)**2

t = int(input().strip())
for a0 in range(t):
    n = int(input().strip())
    print(abs(secondNum(n)-firstNum(n)))

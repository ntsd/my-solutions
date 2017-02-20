#!/bin/python3

#https://www.hackerrank.com/contests/projecteuler/challenges/euler002

def evenFibonacci(n):
    a=1
    b=2
    ans=0
    mode=1
    while 1:
        if mode:
            if a>n:
                return ans
            if a %2==0:
                ans+=a
            a=a+b
            mode=0
        else:   
            if b>n:
                return ans
            if b %2==0:
                ans+=b
            b=a+b
            mode=1
    
t = int(input().strip())
for _ in range(t):
    n = int(input().strip())
    print(evenFibonacci(n))

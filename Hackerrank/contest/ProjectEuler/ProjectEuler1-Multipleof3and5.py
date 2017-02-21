#!/bin/python

#https://www.hackerrank.com/contests/projecteuler/challenges/euler001

def sumOfNaturalNumber(num):
    sum=0
    three=num//3
    five=num//5
    fifteen=num//15
    sum+=3*(three*(three+1)//2) #3* (n+1)*n/2
    sum+=5*(five*(five+1)//2)
    sum-=15*(fifteen*(fifteen+1)//2)
    return sum

t = int(raw_input().strip())
for a0 in xrange(t):
    n = int(raw_input().strip())
    print(sumOfNaturalNumber(n-1))

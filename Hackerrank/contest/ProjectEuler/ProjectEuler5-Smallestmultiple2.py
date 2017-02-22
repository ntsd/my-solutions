from __future__ import division
from fractions import gcd

for _ in range(input()):
    prod = 1
    n = input()
    for i in range(2,n+1):
##        print(prod)
        prod = (prod * i)//gcd(prod,i)
    print prod

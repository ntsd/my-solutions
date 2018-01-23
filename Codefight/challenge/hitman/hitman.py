def hitman(l):
 n=len(l)
 return l[2*(n-2**(len(bin(n))-3))-1]

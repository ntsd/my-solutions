b=""
for c in input():b+='%07d'%int(bin(ord(c))[2:])
print(*("00 "[int(l):]+"0"*len(list(g))for l, g in __import__("itertools").groupby(b)))
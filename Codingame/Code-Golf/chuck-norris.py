print(*("00 "[int(l):]+"0"*len([*g])for l,g in __import__("itertools").groupby(''.join(f'{ord(c):07b}'for c in input()))))
print(*("00 "[l>"0":]+"0"*len([*g])for l,g in __import__("itertools").groupby(''.join(f'{ord(c):07b}'for c in input()))))
print(*("00 "[int(x[0]):]+"0"*len(x)for x in __import__("re").findall('0+|1+',''.join(f'{ord(c):07b}'for c in input()))))
print(*("00 "[x[0]>"0":]+"0"*len(x)for x in __import__("re").findall('0+|1+',''.join(f'{ord(c):07b}'for c in input()))))

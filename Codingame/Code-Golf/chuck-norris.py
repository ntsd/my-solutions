print(*("00 "[int(l):]+"0"*len([*g])for l,g in __import__("itertools").groupby(''.join(f'{ord(c):07b}'for c in input()))))

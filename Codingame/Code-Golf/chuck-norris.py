text = """print(*("00 "[int(l):]+"0"*len([*g])for l,g in __import__("itertools").groupby(''.join(f'{ord(c):07b}'for c in input()))))"""

code = text.encode().decode('utf16')

print(len(code))

print(f"exec(bytes('{code}','u16')[2:])") # Python 3

print(f"exec str(bytearray('{code}','u16')[2:])") # Python 2

# exec(bytes(code,'u16')[2:])
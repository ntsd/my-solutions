text = """i=1
while i<101:print(*[j for j in range(1,i+1)if i%j<1]);i+=1"""

code = text.encode().decode('utf16')

py3 = f"exec(bytes('{code}','u16')[2:])"

py2 = f"exec str(bytearray('{code}','u16')[2:])"

print(py3) # Python 3

print(len(py3))

print(py2) # Python 2

print(len(py2))
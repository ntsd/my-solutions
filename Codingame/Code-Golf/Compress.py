text = """y,n='#\n';print(y*16+n+(y+':'*14+y+n)*6+y*16)"""

code = text.encode().decode('utf16')

py3 = f"exec(bytes('{code}','u16')[2:])"

py2 = f"exec str(bytearray('{code}','u16')[2:])"

print(py3) # Python 3

print(len(py3))

print(py2) # Python 2

print(len(py2))

# exec(bytes(code,'u16')[2:])
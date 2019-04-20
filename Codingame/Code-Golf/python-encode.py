code = """b="".join('%07d'%int(bin(ord(c))[2:])for c in input())
o=b[0]
n=0
for i in b:
 if i!=o:print(["0","00"][i>"0"],"0"*n,end=" ");n=0
 o=i
 n+=1
print(["00","0"][i>"0"],"0"*n,end="")"""
code_encoded = code.encode().decode('utf16')

print(code_encoded)

exec(bytes(code_encoded,'u16')[2:])

# exec(bytes("",'u16')[2:])

code_encoded = code.encode('zlib')

print(code_encoded)

text = code_encoded.decode('zlib')
print(text)
exec(text[2:])

text = """b=""
for c in input():b+='%07d'%int(bin(ord(c))[2:])
o=b[0]
n=0
a=[]
for i in b+"10"[int(b[-1])]:
 if i!=o:a+=["0"*(int(i)+1),"0"*n];n=0
 o=i;n+=1
print(*a)"""

code = text.encode().decode('utf16')

print(len(code))

print(code)

# exec(bytes(code,'u16')[2:])
text = """z=int
b=input
s=str.split
j=s(b())
e={}
e[j[3]]=e['-1']=z(j[4])
for _ in range(z(j[7])):f,q=s(b());e[f]=z(q)
while 1:f,p,d=s(b());print("BWLAOICTK"[[e[f]<=z(p),e[f]>=z(p)][d[0]>"L"]::2])"""

code = text.encode().decode('utf16')

print(len(code))

print(code)

exec(bytes(code,'u16')[2:])

#method 2 use zlib but not work


##code = text.encode("zlib")
##
##print(code)
##
##exec(code.decode("zlib"))

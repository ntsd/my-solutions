b="".join('%07d'%int(bin(ord(c))[2:])for c in input())
o=b[0]
n=0
for i in b:
 if i!=o:print(["0","00"][i>"0"],"0"*n,end=" ");n=0
 o=i
 n+=1
print(["00","0"][i>"0"],"0"*n,end="")
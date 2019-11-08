a=5**.5
for i in range(31):print(round((.5+a/2)**i/a))


print(0)
for i in range(30):x,y=0,1;exec('x,y=y,x+y;'*i);print(y)

f=lambda n:n>1and f(n-1)+f(n-2)or 1
for i in range(31):print(f(i))

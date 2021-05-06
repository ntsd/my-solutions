x,y,a,b=map(int,input().split())
while 1:print("NS"[y>b]*(y!=b)+"WE"[x>a]*(x!=a));b+=[-1,1][y>b]*(y!=b)
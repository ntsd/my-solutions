x,y,a,b=map(int,input().split())
while 1:print(["","S"][y>b]+["",["W","E"][x>a]][x!=a]);b+=1

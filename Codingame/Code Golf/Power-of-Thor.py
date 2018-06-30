code = """x,y,a,b=map(int,input().split())
while 1:print(["","S"][y>b]+["","WE"[x>a]][x!=a]);b+=1 """.encode().decode('utf16')

print(code)

# exec(bytes(code,'u16')[2:])

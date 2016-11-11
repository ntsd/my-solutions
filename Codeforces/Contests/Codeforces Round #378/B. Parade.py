num = int(input())
lis = []
origin = 0
for _ in range(num):
    inp = list(map(int, input().split()))
    origin += inp[0]-inp[1]
    lis.append(inp)
ma = abs(origin)
ma_index = 0
for i in range(num):
    tmp = lis[i][1]-lis[i][0]
    su = abs(origin-(lis[i][0]-lis[i][1])+tmp)
    if su > ma:
        ma = su
        ma_index = i+1
print(ma_index+0)

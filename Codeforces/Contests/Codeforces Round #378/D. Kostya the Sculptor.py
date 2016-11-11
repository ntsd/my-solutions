num = int(input())
ma = 0
stone_choose = set()
stones = set()
for n in range(num):
    c = tuple(map(int,input().split()+[n]))
    tmp = min(c[:-1])
    tmp_index = [n]
    for i in stones:
        if c[0] == i[0] and c[1] == i[1]:
            tmp2 = min(c[0],c[2] + i[2],c[1])
            if tmp2 > tmp:
                tmp = tmp2
                tmp_index = (i[3], n)
        elif c[0] == i[0] and c[2] == i[2]:
            tmp2 = min(c[0],c[1] + i[1],c[2])
            if tmp2 > tmp:
                tmp = tmp2
                tmp_index = (i[3], n)
        elif c[1] == i[1] and c[2] == i[2]:
            tmp2 = min(c[1],c[0] + i[0],c[2])
            if tmp2 > tmp:
                tmp = tmp2
                tmp_index = (i[3], n)
    if tmp > ma:
        ma = tmp
        stone_choose = tmp_index
    stones.add(c)
##    print(stones)
print(len(stone_choose))
ans = ""
for i in stone_choose:
    ans+=str(i+1)+" "
print(ans[:-1])

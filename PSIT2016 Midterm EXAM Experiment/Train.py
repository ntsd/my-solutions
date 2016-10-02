"""..."""
def train(station1, station2):
    """..."""
    lis = []
    for string in (station1, station2):
        letter = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        let = 0
        num = ""
        loop = 0
        for i in string[::-1]:
            if i in letter:
                let += (26**loop)*letter.index(i)
                loop += 1
            else:
                num = i + num
        lis.append([let, int(num)])
    print(abs(lis[0][0]-lis[1][0])+abs(lis[0][1]-lis[1][1]))
train(input(), input())

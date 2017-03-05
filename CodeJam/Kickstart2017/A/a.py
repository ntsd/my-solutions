
def squareCounting(n1, n2):
    n3 = n1-1
    last = 0
    n4 = n3
    for i in range(1,n3+1):
        last+=i*n4
        n4-=1
    print(n2-n1, last)
    if n1 == 2:
        return n2-1
    elif n1 == 3:
        return 2+(n2-n3)*last
    elif n1 == 4:
        return 10+(n2-n3)*last
    elif n1 == 5:
        return 30+(n2-n3)*last
    elif n1 == 6:
        return 70+(n2-n3)*last
    elif n1 > 6:
        return (n2-n3)*last

if __name__ == "__main__":
    t = int(input())
    for i in range(1, t + 1):
        n1, n2 = [int(i) for i in input().split()]
        minN = min(n1, n2)
        maxN = max(n1, n2)
        ans = squareCounting(minN, maxN)
        print("Case #{}: {}".format(i, ans))

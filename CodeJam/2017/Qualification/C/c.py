import math
def bathroomStalls(n, k):
    m = round(n/k)
    m2 = math.floor(n/k)
    return [m, m2]

if __name__ == "__main__":
    t = int(input())
    for i in range(1, t + 1):
        n, k = [int(i) for i in input().split()]
        ans = bathroomStalls(n-2, k+1)
        print("Case #{}: {} {}".format(i, ans[0], ans[1]))

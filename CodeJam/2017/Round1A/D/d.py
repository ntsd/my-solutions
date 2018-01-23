







if __name__ == "__main__":
    t = int(input())
    for i in range(1, t + 1):
        n1 = input()
        ans = tidyNumbers(n1)
        print("Case #{}: {}".format(i, ans))

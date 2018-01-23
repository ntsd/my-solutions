
def tidyNumbers(strNum):
##    print(strNum)
    lenght = len(strNum)
    if lenght == 1:
        return strNum[0]
    
    for i in range(lenght-1,0,-1):
        if any(int(strNum[i]) < int(j) for j in strNum[:i]):
            strNum[i] = "9"
            if strNum[i-1]=="0": strNum[i]="9"
            else:strNum[i-1] = int(strNum[i-1])-1
    for _ in range(lenght):
        for i in range(lenght-1,0,-1):
            if any(int(strNum[i]) < int(j) for j in strNum[:i]):
                strNum[i] = "9"
    return int("".join(str(i) for i in strNum))

if __name__ == "__main__":
    t = int(input())
    for i in range(1, t + 1):
        n1 = input()
        ans = tidyNumbers(list(n1))
        print("Case #{}: {}".format(i, ans))

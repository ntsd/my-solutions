"""
3
5
5 6 8 4 3
3
8 9 7
4
1 3 2 4
"""
def troubleSort(n, nums):
    odd=sorted(nums[::2])
    even=sorted(nums[1::2])
    for i in range(n-1):
        if i % 2 == 0 and odd[i//2] > even[i//2]:
            return i
        elif i % 2 == 1 and even[i//2] > odd[i//2 + 1]:
            return i
    return 'OK'

if __name__ == "__main__":
    for i in range(1, int(input())+1):
        n = int(input())
        nums=list(map(int, input().split()))
        ans = troubleSort(n, nums)
        print("Case #{}: {}".format(i, ans))

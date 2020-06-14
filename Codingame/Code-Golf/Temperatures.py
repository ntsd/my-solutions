input()
print(max((-int(i)**2,i)for i in input().split()or"0")[1])

input()
print(max(input().split()or"0",key=lambda i:(-int(i)**2,i)))

input()
print(min(map(int,input().split()or"0"),key=lambda x:2*x*x-x))

input()
print(max(input().split()or"0",key=lambda x:(-int(x)**2,x)))

input()
print(min(input().split()or"0",key=lambda x:sum(map(ord,x))))

input()
print((min(sorted(map(int,input().split()or'0'))[::-1],key=abs)))
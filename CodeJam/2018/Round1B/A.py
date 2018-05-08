

def Rounding(n,l,c):
    #best = .5000000001

    j=100/n
    ans=0
    lis=[]
    s=0
    for i in c:
        s+=i
        i=j*i
        if i%1>=0.5 or i%1==0:
            ans+=round(i)
        else:
            lis.append(i)
    left=n-s
    lis=sorted(lis, key=lambda x:x%0.5, reverse=True)
    #sort=sorted(lis)
    #print(left, j, ans, lis)
    if j%1>=0.5 or j%1==0:
        ans+=round(j)*left
    else:
        for _ in range(left):
            if len(lis)>0:
                lis[0] += j
                if lis[0]%1>0.5 or lis[0]%1==0:
                    ans+=round(lis.pop(0))
            else:
                lis.append(j)
                
    #print(lis)
    return ans+sum(round(i) for i in lis)

for i in range(int(input())):
    n,l=map(int,input().split())
    c=[int(i) for i in input().split()]
    a=Rounding(n,l,c)
    print('Case #{}: {}'.format(i+1, a))
    

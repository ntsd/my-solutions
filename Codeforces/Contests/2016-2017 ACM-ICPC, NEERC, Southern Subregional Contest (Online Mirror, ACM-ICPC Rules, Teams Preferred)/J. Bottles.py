
    

num_bottle = int(input())
water_in = [int(i) for i in input().split()]
full_bottle = [int(i) for i in input().split()]
n = [i[0] for i in sorted(enumerate(full_bottle), key=lambda x:x[1])]

def checknum():
    return [i!=0 for i in water_in].count(True)

##print(n, checknum())
mi = 0
ma = -1
tmp_num = checknum()
time = 0
mode = 0
tmp_mi = 0
ans = []
while 1:
    try:
        if water_in[n[ma]] +  water_in[n[mi]] >= full_bottle[n[ma]]:
            diff = full_bottle[n[ma]]-water_in[n[ma]]
            water_in[n[mi]] -= diff
            water_in[n[ma]] = full_bottle[n[ma]]
            time += diff
            ma-=1
            mode = 0
        if water_in[n[ma]] +  water_in[n[mi]] < full_bottle[n[ma]]:
            time+=water_in[n[mi]]
            water_in[n[ma]] += water_in[n[mi]]
            water_in[n[mi]] = 0
            mi+=1
            mode = 1
        print(water_in, full_bottle, n[ma], n[mi])
        check = checknum()
        ans.append((check,time))
        if (tmp_num == check and mode) or n[ma] >= n[mi]:
            break
        tmp_num = check
        
    except:
        break
ans2 = min(ans)
print(ans2[0], ans2[1])
        
        
    

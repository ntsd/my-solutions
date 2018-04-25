

def waffle_check(r,c,h,v,waffle, chocolate):
    waffle_h = waffle
    waffle_v = list(zip(*waffle))
    #print(waffle_h, waffle_v)
        
    #holizon
    h_list = []
    target_chocolate_h = chocolate//(h+1)
    chocolate_count=0
    for i in range(r-1):
        chocolate_count+=waffle_h[i].count('@')
        #print('hol', chocolate_count, target_chocolate_h)
        if chocolate_count==target_chocolate_h:
            h_list.append(i+1)
            chocolate_count=0
    
    h_list.append(r)
    #print('h',h_list, target_chocolate_h)
    
    #vertical
    v_list = []
    target_chocolate_v = chocolate//(v+1)
    chocolate_count=0
    for i in range(c-1):
        chocolate_count+=waffle_v[i].count('@')
        #print('hol', chocolate_count, target_chocolate_h)
        if chocolate_count==target_chocolate_v:
            v_list.append(i+1)
            chocolate_count=0
    
    v_list.append(c)
    #print('v',v_list, target_chocolate_v)
    
    if len(h_list)<h+1 or len(v_list) < v+1:
        return "IMPOSSIBLE"
    
    target_chocolate_hv = None
    #print(h,v, 'target', target_chocolate_hv)
    o_h=0
    for h in h_list:
        o_v=0
        for v in v_list:
            count=sum(waffle[o_v:v].count('@') for waffle in waffle_h[o_h:h])
            print(o_h, h, o_v, v, count, waffle_h[o_h:h][0][o_v:v])
            if target_chocolate_hv is None:
                target_chocolate_hv = count
            if count!=target_chocolate_hv:
                return "IMPOSSIBLE"
            o_v=v
        o_h=h
    
    return "POSSIBLE"

for i in range(int(input())):
    r,c,h,v=map(int,input().split())
    waffle=[]
    chocolate=0
    for _ in range(r):
        z = list(input())
        chocolate+=z.count('@')
        waffle.append(z)
    a=waffle_check(r,c,h,v,waffle, chocolate)
    print('Case #{}: {}'.format(i+1, a))
    

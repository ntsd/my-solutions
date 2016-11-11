def delete():
    num_file,num_delete = map(int, input().split())
    list_file = []
    for i in range(num_file):
        list_file.append(input())
    delete_file = [int(i)-1 for i in input().split()]
    ans=[]
    delete_list = sorted([list_file[i]for i in delete_file],key=len)
##    print(delete_list)
    tmp = list(delete_list[0])
    for i in delete_list[1:]:
        name = list(i)
        if len(tmp) != len(i):
            ans.append(tmp)
            tmp=list(i)
        for j in range(len(tmp)):
            if name[j] != tmp[j]:
                tmp[j] = "?"
    ans.append(tmp)
##    print(ans)
    for i in []+ans:
        tmp = i[0]
        p = 1
        for j in i:
            if tmp != j:
                p=0
##        print(i, [j!='?' for j in i])
        if p or all([j!='?' for j in i]):
            ans.remove(i)
    if len(ans) == 0 or len(ans)>1:
        print("No")
    else:
        print("Yes")
        zzz = ""
        for i in ans:
            for c in i:
                zzz+=c
            zzz+=" "
        print(zzz[:-1])
delete()
            
    

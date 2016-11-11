with open('Input.txt', 'r') as f:
    try:
        height,width = [int(i) for i in f.readline().split()]
        upper_2line = []
        upper_line = []
        ans = 0
        for _ in range(height+1):
            line = chr(45)+f.readline()+chr(45)
            this_line = []
            for j, v in enumerate(line):
                if ord(v) == 43:
                    if j not in upper_line:
                        ans+=1
                    else:
                        if ord(line[j-1]) == 45:
                            ans+=1
                        elif ord(line[j+1]) == 45:
                            ans+=1
                    this_line.append(j)
                else:
                    if j+1 in upper_line and j-1 in upper_line and j in upper_line and j in upper_2line:
                        ans+=1
            upper_2line = upper_line
            upper_line = this_line
        print(ans)
    except:
        pass
            


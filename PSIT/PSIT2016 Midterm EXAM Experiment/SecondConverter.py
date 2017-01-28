def secondconverter(num, second, minute, hour):
    """...."""
    hou = num//(minute*second)
    minu = (num-(hou*minute*second))//second
    sec = num-(minu*second)-(hou*minute*second)
    #print(hou, minu, sec)
    return str(hou%hour)+":"+str(minu)+":"+str(sec)

print(secondconverter(int(input()), int(input()), int(input()), int(input())))

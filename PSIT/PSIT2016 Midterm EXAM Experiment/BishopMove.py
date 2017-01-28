def bishopmove():
    """1,2 0,1 2,3 0,3 2,1 3,0"""
    row = int(input())
    col = int(input())
    row, col = col, row
    qx1 = int(input())
    qy1 = int(input())
    bx1 = int(input())
    by1 = int(input())
    bo1 = int(input())
    tx1 = int(input())
    ty1 = int(input())
    #target in way
    if qx1-qy1 == tx1-ty1 or qy1-tx1 == ty1-qx1:
        if qx1-qy1 == bx1-by1 or qy1-bx1 == by1-qx1 \
           and tx1-ty1 == bx1-by1 or ty1-bx1 == by1-tx1:#bishop in way
            if bx1 == tx1 and by1 == ty1:
                if bo1:
                    print("Yes")
                else:
                    print("No")
            else:
                #bishop between way
                if bx1 in list(range(min([qx1, tx1]), max([qx1, tx1]))) \
                   and by1 in list(range(min([qy1, ty1]), max([qy1, ty1]))):
                    print("No")
                else:
                    print("Yes")
        else:
            print("Yes")
    else:
        print("No")
bishopmove()

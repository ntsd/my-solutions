"""4,2 2,4 0,6"""
def bishopmove():
    """1,2 0,1 2,3 0,3 2,1 3,0"""
    row, col = int(input()), int(input())
    row, col = col, row
    qx1 = int(input())
    qy1 = int(input())
    bx1 = int(input())
    by1 = int(input())
    bo1 = int(input())
    tx1 = int(input())
    ty1 = int(input())
    if qx1-qy1 == tx1-ty1 or qy1-tx1 == ty1-qx1:
        if bx1 == tx1 and by1 == ty1:
            if bo1:
                return "Yes"
            return "No"
        if bx1 in [range(min(qx1, tx1), max(qx1, tx1))] \
           and by1 in list(range(min(qy1, ty1), max(qy1, ty1))):
            return "No"
        return "Yes"
    return "No"
print(bishopmove())

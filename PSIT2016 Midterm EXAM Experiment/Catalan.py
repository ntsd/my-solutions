"""..."""
def catalan(num, bnum):
    """..."""
    for i in range(num):
        bnum = ((4*i)+2)/(i+2)*bnum
    return int(bnum)
print(catalan(int(input()), 1))

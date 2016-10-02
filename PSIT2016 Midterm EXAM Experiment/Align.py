"""..."""
def align(space, ali, word):
    """..."""
    if ali == "left":
        print(word)
    elif ali == "right":
        print(" "*(space-len(word))+word)
    elif ali == "center":
        num = space/2-len(word)/2
        if num%1 != 0:
            num = num+1
        print(" "*(int(num))+word)
align(int(input()), input(), input())

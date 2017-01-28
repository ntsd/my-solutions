def check(line):
    """..."""
    reserve = """if else elif while for True False continue break
    return is in and or from as pass not def None""".split()
    special = '!"#$%&\'()*+,-./:;<=>?@[\\]^`{|}~'
    if len(line.split(" ")) > 1:
        return "Invalid"
    if line[0] in "0123456789":
        return "Invalid"
    for j in reserve:
        if j == line:
            return "Invalid"
    for j in special:
        if j in line:
            return "Invalid"
    return "Valid"
def validvar():
    """..."""
    for _ in range(int(input())):
        line = input()
        print(check(line))
validvar()

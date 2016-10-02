"""1000 700 30% 300*100/1000"""
def pressurize(inside, outside):
    """700 1000 30% -300*100/1000"""
    percent = (outside-inside)*100/inside
    if percent < -30:
        print("Underpressure", end=" ")
    elif percent > 30:
        print("Overpressure", end=" ")
    else:
        print("Safe", end=" ")
    print("%.4f%%"%abs(percent))
pressurize(float(input()), float(input()))

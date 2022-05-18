def solution(n, base):
    cycle = []
    k = len(n)
    return command(cycle, n, k, base)


def command(cycle, n, k, base):
    cycle.append(n)
    x = "".join(sorted(list(n), reverse=True))
    y = "".join(sorted(list(n)))
    x_base10 = int(x, base)
    y_base10 = int(y, base)
    z = numberToBase(x_base10 - y_base10, base)
    len_z = len(z)
    n = "0" * (k - len_z) + z
    if n in cycle:
        return len(cycle) - cycle.index(n)
    return command(cycle, n, k, base)


def numberToBase(x, b):
    s = ""
    while x:
        s = str(x % b) + s
        x //= b
    return s

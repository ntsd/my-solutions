from operator import le


def solution(n, base):
    cycle = []
    k = len(n)
    return command(cycle, n, k, base, 0)

def command(cycle, n, k, base, count):
    cycle.append(n)
    prev_n = n
    x = "".join(sorted(list(n), reverse=True))
    y = "".join(sorted(list(n)))
    x_base10 = int(x, base)
    y_base10 = int(y, base)
    z = numberToBase(x_base10 - y_base10, base)
    len_z = len(z)
    n = "0" * (k - len_z) + z
    print('B', cycle, n, k, base, count)
    if n in cycle: # TODO chec it's cycle
        return count
    if prev_n == n:
        return 1
    return command(cycle, n, k, base, count + 1)

def numberToBase(x, b):
    s=""
    while x:
        s = str(x%b) + s
        x//=b
    return s

assert solution('1211', 10) == 1
assert solution('210022', 3) == 3

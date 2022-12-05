def multiplier(a, b):
    return (a - b) / b + 1

def solution(m, f):
    m = int(m)
    f = int(f)
    step = 0
    while True:
        if m <= 0 or f <= 0:
            break
        if m > 100 or f > 100:
            if m > f:
                mul = multiplier(m, f)
                m -= f * mul
                step += mul
            elif f > m:
                mul = multiplier(f, m)
                f -= m * mul
                step += mul
            else:
                break
        else:
            if m > f:
                m -= f
            elif f > m:
                f -= m
            else:
                break
            step += 1
    
    if m == 1 and f == 1 and step >= 0:
        return str(step)
    return 'impossible'

print(solution('2', '1'))
print(solution('3', '13'))
print(solution('3', '14'))
print(solution('4', '5'))
print(solution('4', '6'))
print(solution('4', '7'))
print(solution('4', '9'))
print(solution('4', '10'))
print(solution('4', '11'))

assert solution('4', '7') == '4'
assert solution('2', '1') == '1'

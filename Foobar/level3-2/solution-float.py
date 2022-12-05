def solution(m, f):
    # the m, f can swap
    m, f = float(m), float(f)
    if m == 1:
        return str(int(f - 1))
    if f == 1:
        return str(int(m - 1))
    if f % m == 0 or m % f == 0:
        return "impossible"
    min_bomb = min(m, f)
    max_bomb = max(m, f)
    return str(int((max_bomb / min_bomb) + min_bomb - 1))

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

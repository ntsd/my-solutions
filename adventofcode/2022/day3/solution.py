import string

priority = string.ascii_lowercase + string.ascii_uppercase

f = open('input.txt', 'r')

score = 0

while 1:
    line = f.readline()
    if line == '':
        break
    line = line.strip()
    mid = len(line)//2
    first, second = line[:mid], line[mid:]
    first_set, second_set = set(first), set(second)
    z = first_set.intersection(second_set)
    for i in z:
        score += priority.index(i) + 1

print(score)
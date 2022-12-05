import string

priority = string.ascii_lowercase + string.ascii_uppercase

f = open('input.txt', 'r')

score = 0

lines = []
i = 0

while 1:
    if i % 3 == 0 and i != 0:
        lines_set = list(map(set, lines))
        intersect = lines_set[0].intersection(lines_set[1]).intersection(lines_set[2])
        for letter in intersect:
            score += priority.index(letter) + 1
        lines = []

    line = f.readline()
    if line == '':
        break
    line = line.strip()

    
    lines.append(line)
    i+=1

print(score)
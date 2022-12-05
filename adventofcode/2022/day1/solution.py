f = open('input.txt', 'r')

max_cal = 0
cur_cal = 0
sum_cal = []

while 1:
    line = f.readline()
    if line == "\n":
        sum_cal.append(cur_cal)
        cur_cal = 0
        continue
    if line == '':
        break
    cur_cal += int(line.strip())
    if cur_cal > max_cal:
        max_cal = cur_cal
    

print(max_cal)

sum_cal.sort(reverse=1)

print(sum(sum_cal[:3]))

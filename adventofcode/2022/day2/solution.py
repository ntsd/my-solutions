f = open('input.txt', 'r')

shape_score = {
    "X": 1,
    "Y": 2,
    "Z": 3,
}

score_result = {
    "A": {
        "X": 3,
        "Y": 6,
        "Z": 0,
    },
    "B": {
        "X": 0,
        "Y": 3,
        "Z": 6,
    },
    "C": {
        "X": 6,
        "Y": 0,
        "Z": 3,
    },
}

win_score = {
    "X": 0,
    "Y": 3,
    "Z": 6,
}

win_shape = {
    "A": {
        "X": "Z",
        "Y": "X",
        "Z": "Y",
    },
    "B": {
        "X": "X",
        "Y": "Y",
        "Z": "Z",
    },
    "C": {
        "X": "Y",
        "Y": "Z",
        "Z": "X",
    },
}

sum_score = 0
sum_score_2 = 0

while 1:
    line = f.readline()
    if line == '':
        break
    op, my = line.split()
    sum_score += score_result[op][my] + shape_score[my]

    sum_score_2 += win_score[my] + shape_score[win_shape[op][my]]

print(sum_score)

print(sum_score_2)

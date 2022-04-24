def solution(s):
    cake_radius = len(s)
    first_color  = s[0]
    sequence_lenght = 1
    for i in range(1, cake_radius):
        if first_color == s[i] and cake_radius % sequence_lenght == 0:
            split_num = cake_radius // sequence_lenght
            if checkIsSequence(s, sequence_lenght, split_num):
                return split_num
        sequence_lenght += 1
        if sequence_lenght > cake_radius / 2.0:
            break
    return 1

def checkIsSequence(s, sequence_lenght, split_num):
    for sequence_pos in range(sequence_lenght):
        check_color = s[sequence_pos]
        for split_pos in range(1, split_num):
            if s[split_pos * sequence_lenght + sequence_pos] != check_color:
                return False
    return True

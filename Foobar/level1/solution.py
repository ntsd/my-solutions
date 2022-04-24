def solution(s):
    cake_radius = len(s)
    
    first_color  = s[0]
    mam_sequence = [first_color]
    sequence_lenght = 1
    for i in range(1, cake_radius):
        if first_color == s[i]:
            print('mam_sequence', mam_sequence)
            # check it can split to same amount of pieces
            if cake_radius % sequence_lenght == 0:
                split_num = cake_radius // sequence_lenght
                if checkIsSequence(s, sequence_lenght, split_num):
                    return split_num
        mam_sequence.append(s[i])
        sequence_lenght += 1
        print('sequence_lenght > cake_radius / 2', sequence_lenght, cake_radius / 2.0)
        # break when it's more than half of the cake
        if sequence_lenght > cake_radius / 2.0:
            break
    return 1

def checkIsSequence(s, sequence_lenght, split_num):
    print('split_num, sequence_lenght', split_num, sequence_lenght)
    for sequence_pos in range(sequence_lenght):
        check_color = s[sequence_pos]
        for split_pos in range(1, split_num):
            print(s[split_pos * sequence_lenght + sequence_pos], check_color)
            if s[split_pos * sequence_lenght + sequence_pos] != check_color:
                return False
    return True

assert solution("ABCABCABCABC") == 4
assert solution("ABABAB") == 3
assert solution("AAAAA") == 5
assert solution("ABACABACABAC") == 3
assert solution("DCABDCABDCAB") == 3
assert solution("ABCDE") == 1
assert solution("ABCDEF") == 1
assert solution("A") == 1
assert solution("AB") == 1
assert solution("BBBB") == 4
assert solution("aassccaasscc") == 2
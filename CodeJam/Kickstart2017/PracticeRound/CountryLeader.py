def getLenghtAlphabet(string):
    alphabet = []
    lenght = 0
    char = 0
##    minAlphabet = None
    for i in string:
        if i != " ":
            char+=1
            if i not in alphabet:
                alphabet.append(i)
                lenght+=1
##    print(lenght, char)
    return [lenght, char]

def countryLeader(num):
    maxWord = None
    maxAlphaber = [0, 0]
    for i in range(num):
        string = input()
        new = getLenghtAlphabet(string)
        if new[0] > maxAlphaber[0]:
            maxAlphaber = new
            maxWord = string
        elif new[0] == maxAlphaber[0] and new[1] > maxAlphaber[1]:
            maxAlphaber = new
            maxWord = string
    return maxWord

if __name__ == "__main__":
    t = int(input())
    for i in range(1, t + 1):
        l = int(input())
        ans = countryLeader(l);
        print("Case #{}: {}".format(i, ans))

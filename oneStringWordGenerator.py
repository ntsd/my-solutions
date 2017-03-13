def oneStringWordGenerator(string, part):
    oneString = ""
    lenght = len(string)
    string = string+" "*(lenght%part)
    lenght+=lenght%part
    charPerPart = lenght//part
    strings=[string[c*charPerPart:c*charPerPart+charPerPart] for c in range(part)]
    maxString = max([len(i) for i in strings])
    for i in range(maxString):
        for c in strings:
            try:
                oneString+=c[i]
            except:
                oneString+=""
##    print("".join(oneString[i::part] for i in range(part)))
    return oneString

word = "Hello World"
part = 2
assert  oneStringWordGenerator(word, part) == "HWeolrllod  "

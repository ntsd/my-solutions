def Readmore(test):
    if len(test)<=55:
        print(test)
    else:
        string = test[:40]
        if string[-1]==" " and string[-2] != " ":
            print(string[:-1]+"... <Read More>")
        elif string[-2]==" ":
            print(string[:-2]+"... <Read More>")
        else:
            space = 1
            for c in string[::-1]:
                if c == " ":
                    break
                space+=1
            print(string[:-space]+"... <Read More>")

assert(2 + 2 == 5, "Houston we've got a problem")

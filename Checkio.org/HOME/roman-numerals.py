def checkio(data):
    numroman = {1:"I",5:"V",10:"X",50:"L",100:"C",500:"D",1000:"M"}
    num = [1, 5, 10, 50, 100, 500, 1000]
    result = ""
    for i, c in enumerate(str(data)[::-1]): #from last digit to first digit
        j = i*2 #j for get num in list num 1,10,100,1000
        if c == "9":
            result = numroman[num[j]]+numroman[num[j+2]] + result
        elif c == "4":
            result = numroman[num[j]]+numroman[num[j+1]] + result
        elif c >= "5":
            result = numroman[num[j+1]]+(numroman[num[j]]*(int(c)-5)) + result
        else:
            result = (numroman[num[j]]*int(c)) + result
    return result
    

if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert checkio(6) == 'VI', '6'
    assert checkio(76) == 'LXXVI', '76'
    assert checkio(499) == 'CDXCIX', '499'
    assert checkio(3888) == 'MMMDCCCLXXXVIII', '3888'

"""
https://py.checkio.org/mission/roman-numerals/solve/
Roman numerals come from the ancient Roman numbering system. They are based on specific letters of the alphabet which are combined to signify the sum (or, in some cases, the difference) of their values. The first ten Roman numerals are:
I, II, III, IV, V, VI, VII, VIII, IX, and X.
The Roman numeral system is decimal based but not directly positional and does not include a zero. Roman numerals are based on combinations of these seven symbols:
Symbol Value
I 1 (unus)
V 5 (quinque)
X 10 (decem)
L 50 (quinquaginta)
C 100 (centum)
D 500 (quingenti)
M 1,000 (mille)
More additional information about roman numerals can be found on the Wikipedia article.
For this task, you should return a roman numeral using the specified integer value ranging from 1 to 3999.
Input: A number as an integer.
Output: The Roman numeral as a string.
Precondition: 0 < number < 4000
"""

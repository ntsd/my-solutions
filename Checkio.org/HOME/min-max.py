def min(*args, **kwargs):
    key = kwargs.get("key", None)
    print(type(args[0]), key)
    if type(args[0]) == int or type(args[0]) == float:
        check = args
        m = 9999999999999999
    elif type(args[0]) == list or type(args[0]) == tuple:
        check = args[0]
        m = 9999999999999999
    elif type(args[0]) == str:
        check = args[0]
        m = chr(255)
##    elif type(args[0]) == range:
    else:
        check = list(args[0])
        m = 9999999999999999
    check2 = check
    if key != None:
        check2 = map(key, check)
    print(check2, check)
    try:
        m = 9999999999999999
        for n, i in enumerate(check2):
            if i < m:
                m = i
                num = n
    except:
        m = chr(255)
        for n, i in enumerate(check2):
            if i < m:
                m = i
                num = n
    return check[num]

def max(*args, **kwargs):
    key = kwargs.get("key", None)
    print(type(args[0]), key)
    if type(args[0]) == int or type(args[0]) == float:
        check = args
    elif type(args[0]) == list or type(args[0]) == tuple:
        check = args[0]
    elif type(args[0]) == str:
        check = args[0]
##    elif type(args[0]) == range:
    else:
        check = list(args[0])
    check2 = check
    if key != None:
        check2 = list(map(key, check))
    print(check2, check)
    try:
        m = -9999999999999999
        for n, i in enumerate(check2):
            if i > m:
                m = i
                num = n
    except:
        m = chr(0)
        for n, i in enumerate(check2):
            if i > m:
                m = i
                num = n
    return check[num]

if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert max(3, 2) == 3, "Simple case max"
    assert min(3, 2) == 2, "Simple case min"
    assert max([1, 2, 0, 3, 4]) == 4, "From a list"
    assert min("hello") == "e", "From string"
    assert max(2.2, 5.6, 5.9, key=int) == 5.6, "Two maximal items"
    assert min([[1, 2], [3, 4], [9, 0]], key=lambda x: x[1]) == [9, 0], "lambda key"
    assert min((9,)) == 9
    assert max(range(6)) == 5
    assert min(abs(i) for i in range(-10, 10)) == 0
    assert max(filter(str.isalpha,"@v$e56r5CY{]"))
    assert max([1, 2, 3], [5, 6], [7], [0, 0, 0, 1]) == [7]
"""
https://py.checkio.org/mission/min-max/solve/
In this mission you should write you own py3 implementation (but you can use py2 for this) of the built-in functions min and max. Some builtin functions are closed here: import, eval, exec, globals. Don't forget you should implement two functions in your code.
max(iterable, *[, key]) or min(iterable, *[, key])
max(arg1, arg2, *args[, key]) or min(arg1, arg2, *args[, key])
Return the largest (smallest) item in an iterable or the largest(smallest) of two or more arguments.
If one positional argument is provided, it should be an iterable. The largest (smallest) item in the iterable is returned. If two or more positional arguments are provided, the largest (smallest) of the positional arguments is returned.
The optional keyword-only key argument specifies a function of one argument that is used to extract a comparison key from each list element (for example, key=str.lower).
If multiple items are maximal (minimal), the function returns the first one encountered.

-- Python Documentation (Built-in Functions)

Input: One positional argument as an iterable or two or more positional arguments. Optional keyword argument as a function.
Output: The largest item for the "max" function and the smallest for the "min" function.
Precondition: All test cases are correct and functions don't have to raise exceptions.
"""

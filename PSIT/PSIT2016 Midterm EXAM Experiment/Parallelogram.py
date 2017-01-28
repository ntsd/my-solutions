def parallelogram(text):
    """..."""
    lenght = len(text)
    for i in range(1, lenght):
        print(" "*(lenght-i)+text[:i])
    for i in range(lenght):
        print(text[i:])
parallelogram(input())

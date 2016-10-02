"""..."""
def iamback(word):
    """..."""
    letter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    print("Hello "+word+"." if word[0] in letter+letter.lower() else "สวัสดี "+word)
iamback(input())

s = "A"+input()+"A"
vowels = "AEIOUY"
vowels = vowels+vowels.lower()
ma=0
tmp=1
for i in s:
    if i in vowels:
        if tmp > ma:
            ma=tmp
        tmp=1
    else:
        tmp+=1
print(ma)

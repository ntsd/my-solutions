import sys

with open(sys.argv[1], 'r') as test_cases:
    for test in test_cases:
        s1 = test.split()
        ans=""
        for i in s1[::-1]:
            ans+=i+" "
        print(ans[:-1])

import sys

with open(sys.argv[1], 'r') as test_cases:
    for test in test_cases:
        n = int(test)
        if n == 0:
            continue
        max_x = 0
        min_x = 0
        max_y = 0
        min_y = 0
        for _ in range(n):
            inp = input()
            x,y = [int(i) for i in inp.split()]
            if x > max_x:
                max_x = x
            if x < min_x:
                min_x = x
            if y > max_y:
                max_y = y
            if y < min_y:
                min_y = y
        area = (max_x-min_x)*(max_y-min_y)
        print("%.3f"%round(area,3))

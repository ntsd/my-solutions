import sys
#l = [2**i for i in range(33)]
l = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216, 33554432, 67108864, 134217728, 268435456, 536870912, 1073741824, 2147483648, 4294967296]
with open(sys.argv[1], 'r') as test_cases:
    for test in test_cases:
        l = len(test)
        num = int(test)
        n = 0
        for i in range(len(l)):
            if l[i] > num:
                n=i
                break

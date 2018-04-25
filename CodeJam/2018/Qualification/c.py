#!/usr/bin/env python3
import sys


def run():
    t = int(input())

    for c in range(t):
        # target area
        a = int(input())
        print('>>>> a = %d' % a, file=sys.stderr)
        # target W*H
        w = 3
        h = 3
        while w * w < a:
            w += 1
            h += 1
        while h > 3 and w * (h - 1) >= a:
            h -= 1

        print('W*H = %d*%d' % (w, h), file=sys.stderr)

        # the grid
        g = [[False] * (h + 1) for i in range(w + 1)]

        # the indices mapper, empty cell with the center
        m = [set() for i in range(10)]

        for i in range(2, w):
            for j in range(2, h):
                m[9].add((i, j))

        done = False
        k = 9

        while not done:
            while len(m[k]) == 0:
                k -= 1
            i, j = next(iter(m[k]))
            print('put (%d, %d)' % (i, j), file=sys.stderr)
            #print(m, file=sys.stderr)
            print(i, j)
            x, y = map(int, input().split())
            print('get (%d, %d)' % (x, y), file=sys.stderr)
            if x == 0 and y == 0:
                done = True
            elif x == -1 and y == -1:
                exit(1)
            elif not g[x][y]:
                g[x][y] = True
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        xx = x + dx
                        yy = y + dy
                        for kk in range(1, 10):
                            if (xx, yy) in m[kk]:
                                m[kk - 1].add((xx, yy))
                                m[kk].remove((xx, yy))
        print(m, file=sys.stderr)

run()

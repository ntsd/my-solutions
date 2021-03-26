# TODO
# Add one mine in 2 blocks, 3 blocks

import sys
import math
from enum import Enum

w, h = 30, 16


class Type(Enum):
    SAFE = 2
    NUMBER = 1
    REVEAL = 0
    UNKNOWN = -1
    MINE = -2


is_unknown = lambda n: n.type == Type.UNKNOWN
is_mine = lambda n: n.type == Type.MINE
is_safe = lambda n: n.type == Type.SAFE
is_edge = lambda n: n.type != Type.NUMBER and n.type != Type.REVEAL


class Point:
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.value = 0
        self.type = Type.UNKNOWN
        self.neighbors = []
        self.neighbors_edge = []

    def __repr__(self):
        return ':'.join([str(self.x)+','+str(self.y), str(self.value), str(self.type)])


graph = {}
for i in range(h):
    for j in range(w):
        graph[(i, j)] = Point(i, j)

for i in range(h):
    for j in range(w):
        graph[(i, j)].neighbors = list(filter(lambda x: x, [
            graph.get((i-1, j-1), None),
            graph.get((i-1, j), None),
            graph.get((i-1, j+1), None),
            graph.get((i, j-1), None),
            graph.get((i, j+1), None),
            graph.get((i+1, j-1), None),
            graph.get((i+1, j), None),
            graph.get((i+1, j+1), None)
        ]))

# start at middle
for i in range(h):
    input().split()
print(15, 8)

def find_safe(numbers):
    # filter only bround of number neighbors
    edges = []
    for num in numbers:
        num.neighbors_edge = list(filter(is_edge, num.neighbors))
        edges += num.neighbors_edge

    # fill mine with number edge
    for num in numbers:
        if len(num.neighbors_edge) == num.value:
            for n in num.neighbors_edge:
                n.type = Type.MINE

    # fill safe with mine
    for num in numbers:
        mine_neighbor_edge = list(filter(is_mine, num.neighbors_edge))
        if len(mine_neighbor_edge) == num.value:
            for n in num.neighbors_edge:
                if n.type != Type.MINE:
                    n.type = Type.SAFE

    # fill mine from safe
    for num in numbers:
        safe_neighbor_edge = list(filter(is_safe, num.neighbors_edge))
        if len(num.neighbors_edge) - len(safe_neighbor_edge) == num.value:
            for n in num.neighbors_edge:
                if n.type != Type.SAFE:
                    n.type = Type.MINE


    # print(edges, file=sys.stderr)
    # mine edge
    mine_edges = list(filter(is_mine, edges))
    mine_str = ' '.join([str(b.x) + ' ' + str(b.y) for b in mine_edges])

    # sefe edge
    sefe_edges = list(filter(is_safe, edges))
    if len(sefe_edges) > 0:
        print(sefe_edges[0].x, sefe_edges[0].y, mine_str)
        return

    # random
    unknown_edges = list(filter(is_unknown, edges))
    print(unknown_edges[0].x, unknown_edges[0].y, mine_str)

while True:
    numbers = []

    # update graph
    for i in range(h):
        row = input().split()
        for j in range(w):
            if row[j] == "?":
                pass
            elif row[j] == ".":
                graph[(i, j)].type = Type.REVEAL
            else:
                graph[(i, j)].value = int(row[j])
                graph[(i, j)].type = Type.NUMBER
                numbers.append(graph[(i, j)])

    find_safe(numbers)

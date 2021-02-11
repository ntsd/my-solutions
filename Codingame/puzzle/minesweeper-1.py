import sys
import math

w = 30
h = 16

graph = {}

class Point:
    # 0 = ., -1 = ?, -2 = bomb
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.value = -1
        self.neighbors = []
    def __repr__(self):
        return str(self.value)

for i in range(h):
    for j in range(w):
        graph[(i, j)] = Point(i, j)

for i in range(h):
    for j in range(w):
        graph[(i, j)].neighbors = [
            graph.get((i-1, j-1), None),
            graph.get((i-1, j), None),
            graph.get((i-1, j+1), None),
            graph.get((i, j-1), None),
            graph.get((i, j+1), None),
            graph.get((i+1, j-1), None),
            graph.get((i+1, j), None),
            graph.get((i+1, j+1), None)
        ]

while True:
    for i in range(h):
        row = input().split()
        for j in range(w):
            if row[j] == "?":
                pass
            elif row[j] == ".":
                graph[(i, j)].value = 0
            else:
                graph[(i, j)].value = int(row[j])
    
    unknowns = list(filter(lambda x: x.value == -1, graph.values()))

    # random 
    print(unknowns[0].x, unknowns[0].y)
    # print(graph, file=sys.stderr)

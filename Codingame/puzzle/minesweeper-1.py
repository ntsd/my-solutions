import sys
import itertools
from enum import Enum

w, h = 30, 16


class Type(Enum):
    SAFE = 2
    NUMBER = 1
    REVEAL = 0
    UNKNOWN = -1
    MINE = -2


def is_unknown(n): return n.type == Type.UNKNOWN
def is_mine(n): return n.type == Type.MINE
def is_safe(n): return n.type == Type.SAFE
def is_edge(n): return n.type != Type.NUMBER and n.type != Type.REVEAL


def get_unknowns(nodes):
    nodes = list(filter(is_unknown, nodes))
    nodes_len = len(nodes)
    return nodes, nodes_len


def get_mines(nodes):
    nodes = list(filter(is_mine, nodes))
    nodes_len = len(nodes)
    return nodes, nodes_len


def get_safes(nodes):
    nodes = list(filter(is_safe, nodes))
    nodes_len = len(nodes)
    return nodes, nodes_len


class Node:
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.value = 0
        self.type = Type.UNKNOWN
        self.neighbors = []
        self.neighbors_edge = []
        self.neighbors_edge_len = 0

    def __repr__(self):
        return ':'.join([str(self.x)+','+str(self.y), str(self.value), str(self.type)])

    def __hash__(self):
        return hash((self.x, self.y))


graph = {}
for i in range(h):
    for j in range(w):
        graph[(i, j)] = Node(i, j)

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
for _ in range(h):
    input().split()
print(15, 8)


def add_mssp_from_mine(numbers, mssp):
    for num in numbers:
        unknown_edges, unknown_edges_len = get_unknowns(num.neighbors_edge)
        _, mine_neighbor_edge_len = get_mines(
            num.neighbors_edge)
        if num.value - mine_neighbor_edge_len == 1 and unknown_edges_len in [2, 3]:
            one_in_multi = frozenset(unknown_edges)
            mssp[one_in_multi] = unknown_edges_len


def fill_safe_with_mine(numbers, mssp):
    # fill safe with mine
    for num in numbers:
        mine_neighbor_edge, mine_neighbor_edge_len = get_mines(
            num.neighbors_edge)
        if mine_neighbor_edge_len == num.value:
            for n in num.neighbors_edge:
                if n.type != Type.MINE:
                    n.type = Type.SAFE
        # fill safe, mine by dssp
        neighbors_edge_combinations = list(itertools.combinations(
            num.neighbors_edge, 2)) + list(itertools.combinations(num.neighbors_edge, 3))
        for combination in neighbors_edge_combinations:
            frozenset_combination = frozenset(combination)
            if frozenset_combination in mssp:
                if num.value - mine_neighbor_edge_len - 1 == 0 and \
                        num.neighbors_edge_len - mssp[frozenset_combination] - mine_neighbor_edge_len >= 1:
                    print('safe', num, frozenset_combination, file=sys.stderr)
                    for n in frozenset(num.neighbors_edge) - frozenset_combination - frozenset(mine_neighbor_edge):
                        print(
                            combination,
                            "safe from combinations_of_" +
                            str(mssp[frozenset_combination]),
                            n,
                            file=sys.stderr
                        )
                        n.type = Type.SAFE
                if num.value - mine_neighbor_edge_len - 1 == 1 and \
                        num.neighbors_edge_len - mssp[frozenset_combination] - mine_neighbor_edge_len == 1:
                    print('mine', num, frozenset_combination, file=sys.stderr)
                    for n in frozenset(num.neighbors_edge) - frozenset_combination:
                        n.type = Type.MINE
                        print(
                            combination,
                            "mine from combinations_of_" +
                            str(mssp[frozenset_combination]),
                            n,
                            file=sys.stderr
                        )


def fill_mine_with_safe(numbers):
    for num in numbers:
        _, safe_neighbor_edge_len = get_safes(
            num.neighbors_edge)
        if num.neighbors_edge_len - safe_neighbor_edge_len == num.value:
            for n in num.neighbors_edge:
                if n.type != Type.SAFE:
                    n.type = Type.MINE


def find_safe(numbers):
    # filter only bound of number neighbors
    edges = []
    for num in numbers:
        num.neighbors_edge = list(filter(is_edge, num.neighbors))
        num.neighbors_edge_len = len(num.neighbors_edge)
        edges += num.neighbors_edge

    # fill mine with number edge
    for num in numbers:
        if num.neighbors_edge_len == num.value:
            for n in num.neighbors_edge:
                n.type = Type.MINE

    for _ in range(5):  # dept
        # multi set single point: there's a mine belong multi square
        mssp = {}
        add_mssp_from_mine(numbers, mssp)
        fill_safe_with_mine(numbers, mssp)
        fill_mine_with_safe(numbers)

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
    print("random", file=sys.stderr)
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

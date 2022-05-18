import heapq


def solution(src, dest):
    if src == dest:
        return 0
    graph = {}
    for r in range(8):
        for c in range(8):
            pos = r * 8 + c
            if pos not in graph:
                graph[pos] = set()
            for x, y in [
                (c - 1, r - 2),
                (c + 1, r - 2),
                (c - 1, r + 2),
                (c + 1, r + 2),
                (c + 2, r - 1),
                (c + 2, r + 1),
                (c - 2, r - 1),
                (c - 2, r + 1),
            ]:
                if x < 0 or y < 0 or x >= 8 or y >= 8:
                    continue
                graph[pos].add(y * 8 + x)
    return dijkstar_shortest_path(graph, src, dest)


def dijkstar_shortest_path(graph, start, end):
    queue = [(0, start)]
    seen = set()
    shortest = float("inf")
    while True:
        curr_cost, curr = heapq.heappop(queue)
        if curr not in seen:
            seen.add(curr)
            if curr == end:
                if curr_cost < shortest:
                    shortest = curr_cost
                    continue
            for next_ in graph[curr]:
                next_cost = curr_cost + 1
                if next_cost < shortest:
                    heapq.heappush(queue, (next_cost, next_))
        if not queue:
            break
    return shortest


assert solution(0, 1) == 3
assert solution(19, 36) == 1
assert solution(21, 26) == 2

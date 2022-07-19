import heapq


def dijkstar_shortest_path(graph, start, end):
    queue = [(0, start, 0)]  # cost, pos, wall_count (weigth)
    seen = set()
    shortest = float("inf")
    while True:
        if not queue:
            break
        cur_cost, cur_pos, cur_weigth = heapq.heappop(queue)
        if cur_pos not in seen:
            seen.add(cur_pos)
            if cur_pos == end:
                if cur_cost < shortest:
                    shortest = cur_cost
                    continue
            for next_pos in graph[cur_pos]:
                next_weigth = cur_weigth + graph[cur_pos][next_pos]
                next_cost = cur_cost + 1
                if next_cost < shortest and next_weigth <= 1:
                    heapq.heappush(queue, (next_cost, next_pos, next_weigth))
    return shortest


def solution(maze):
    h = len(maze)
    w = len(maze[0])
    graph = {}
    for r, row in enumerate(maze):
        for c, col in enumerate(row):
            pos = (c, r)
            if pos not in graph:
                graph[pos] = {}
            for x, y in [
                (c - 1, r),
                (c + 1, r),
                (c, r - 1),
                (c, r + 1),
            ]:
                if x < 0 or y < 0 or x >= w or y >= h:
                    continue
                graph[pos][(x, y)] = maze[y][x]
    cost = dijkstar_shortest_path(graph, (0, 0), (w - 1, h - 1))
    return cost + 1

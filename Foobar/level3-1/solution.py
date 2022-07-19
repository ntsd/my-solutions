import heapq

def dijkstar_shortest_path(graph, start, end):
    queue = [(0, start, 0)] # cost, pos, wall_count (weigth)
    seen = set()
    shortest = float("inf")
    while True:
        if not queue:
            break
        cur_cost, cur_pos, cur_weigth = heapq.heappop(queue)
        if (cur_pos, cur_weigth) not in seen:
            seen.add((cur_pos, cur_weigth)) # seen with wall count
            if cur_pos == end:
                if cur_cost < shortest:
                    shortest = cur_cost
                    continue
            for next_pos in graph[cur_pos]:
                next_weigth = cur_weigth + graph[cur_pos][next_pos]
                # print(next_pos, next_weigth)
                next_cost = cur_cost + 1
                if next_cost < shortest and next_weigth <= 1:
                    heapq.heappush(queue, (next_cost, next_pos, next_weigth))
    return shortest

def solution(maze):
    h = len(maze)
    w = len(maze[0])
    graph = {}
    for r in range(h):
        for c in range(w):
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
    # print(graph[(0,0)])
    cost = dijkstar_shortest_path(graph, (0,0), (w-1, h-1))
    return cost + 1

print(solution([[1, 0],
                [0, 0],]))

assert solution([
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0],
]) == 7

assert solution([
    [0, 1, 1, 0],
    [0, 0, 0, 1],
    [1, 1, 0, 0],
    [1, 1, 1, 0]
]) == 7

assert solution([
    [0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0]
]) == 11

assert solution([
    [0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0],
    [1, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0]
]) == 13

assert solution([
    [0, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0],
    [1, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0]
]) == 21

assert solution([
    [0]
]) == 1

# TODO fix this
print(solution([
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]))

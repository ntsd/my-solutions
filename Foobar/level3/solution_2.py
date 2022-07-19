import heapq

def get_neighbors(metrix, pos, w, h):
    neighbors = []
    for x, y in [
        (pos[0] - 1, pos[1]),
        (pos[0] + 1, pos[1]),
        (pos[0], pos[1] - 1),
        (pos[0], pos[1] + 1),
    ]:
        if x < 0 or y < 0 or x >= w or y >= h:
            continue
        neighbors.append((x, y))
    return neighbors

def dijkstar_shortest_path(metrix, start, end, w, h):
    queue = [(0, start, 0)] # cost, pos, wall_count (weigth)
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
            # todo change to metrix
            for next_pos in get_neighbors(metrix, cur_pos, w, h):
                next_weigth = cur_weigth + metrix[next_pos[1]][next_pos[0]]
                # print(next_pos, next_weigth)
                next_cost = cur_cost + 1
                if next_cost < shortest and next_weigth <= 1:
                    heapq.heappush(queue, (next_cost, next_pos, next_weigth))
    return shortest

def solution(metrix):
    h = len(metrix)
    w = len(metrix[0])
    cost = dijkstar_shortest_path(metrix, (0,0), (w-1, h-1), w, h)
    return cost + 1

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

import sys
import math
import heapq
from copy import deepcopy

def getDiraction(old, new):
    if new[0] < old[0]:
        return "LEFT"
    if  new[0] > old[0]:
        return "RIGHT"
    if new[1] < old[1]:
        return "UP"
    if  new[1] > old[1]:
        return "DOWN"
    return "NONE"

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Wall:
    def __init__(self, x, y, orientation):
        self.x = x
        self.y = y
        self.orientation = orientation # ('H' or 'V')
    
    def isCross(self, other):
        if self.orientation == other.orientation\
        and self.x == other.x and self.y == other.y:
            return True
        if self.orientation == 'V' and other.orientation == 'V'\
        and self.x == other.x and abs(self.y-other.y)<2:
            return True
        if self.orientation == 'H' and other.orientation == 'H'\
        and self.y == other.y and abs(self.x-other.x)<2:
            return True
        if self.orientation != other.orientation:
            if self.orientation == 'H' and self.x==other.x+1 and self.y==other.y-1:
                return True
            elif self.x==other.x-1 and self.y==other.y+1:
                return True
        return False
    
    def __repr__(self):
        return '{} {} {}'.format(self.x, self.y, self.orientation)
    
    def __str__(self):
        return '{} {} {}'.format(self.x, self.y, self.orientation)
    
    def __hash__(self):
        return hash(self.x) ^ hash(self.y) ^ hash(self.orientation)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.orientation == other.orientation

def shortest_path_closet(graph, start, ends):
    """ return cost, path, end """
    if type(start) is not tuple:
        start = (start.x, start.y)
    queue = [(0, start, [])]
    seen = set()
    while True:
        (cost, v, path) = heapq.heappop(queue)
        if v not in seen:
            path = path + [v]
            seen.add(v)
            for e in ends:
                if v[0] == e.x and v[1] == e.y:
                    return cost, path, e
            for next_ in graph[v]:
                heapq.heappush(queue, (cost + 1, next_, path))
        if len(queue) ==0: # no way to target
            return -1, [], None
            

class Player:
    def __init__(self, id, targets):
        self.id = id
        self.targets = targets
    
    def update(self):
        self.x, self.y, self.walls_left = [int(j) for j in input().split()]

    def __repr__(self):
        return '{} {} {] {]'.format(self.id, self.x, self.y, self.walls_left)
    
    def __str__(self):
        return '{} {} {] {]'.format(self.id, self.x, self.y, self.walls_left)
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def score(self, graph):
        cost, path, end = shortest_path_closet(graph, self, self.targets)
        if cost == -1: # no way run
            return -1
        return cost
    
# w: width of the board
# h: height of the board
# player_count: number of players (2 or 3)
# my_id: id of my player (0 = 1st player, 1 = 2nd player, ...)
w, h, player_count, my_id = [int(i) for i in input().split()]

graph={}
targets=[[] for _ in range(3)]
for y in range(h):
    for x in range(w):
        neighbours = []
        if x < w-1:
            neighbours.append((x + 1, y))
        else:
            targets[0].append(Point(x, y))
        if x > 0:
            neighbours.append((x - 1, y))
        else:
            targets[1].append(Point(x, y))
        if y < h-1:
            neighbours.append((x, y + 1))
        else:
            targets[2].append(Point(x, y))
        if y > 0:
            neighbours.append((x, y - 1))
        graph[(x, y)] = neighbours 

def action(): # action: LEFT, RIGHT, UP, DOWN or "putX putY putOrientation" to place a wall
    my_player = players[my_id]
    op_players = [p for p in players if p.id!=my_id and p.x != -1]
    
    best_cost, best_path, end = shortest_path_closet(graph, my_player, my_player.targets)
    
    if my_player.walls_left > 0 and len(op_players)==1:
        simulate_walls =[]
        for wall_y in range(1, h): # check 'H' wall # todo reduce time
            for wall_x in range(0, w-1, 2):
                wall = Wall(wall_x, wall_y, 'H')
                # print(wall_x, wall_y, file=sys.stderr)
                if not any(wall.isCross(w) for w in walls):
                    graph_temp = deepcopy(graph)
                    graph_temp[(wall_x, wall_y)].remove((wall_x, wall_y-1))
                    graph_temp[(wall_x, wall_y-1)].remove((wall_x, wall_y))
                    graph_temp[(wall_x+1, wall_y)].remove((wall_x+1, wall_y-1))
                    graph_temp[(wall_x+1, wall_y-1)].remove((wall_x+1, wall_y))
                    # check score
                    my_score = my_player.score(graph_temp)
                    if best_cost - my_score == 0:
                        op_score = sum([op.score(graph_temp) for op in op_players])
                        simulate_walls.append((op_score, wall))
        for wall_y in range(0, h-1, 2): # check 'V' wall # todo reduce time
            for wall_x in range(1, w):
                wall = Wall(wall_x, wall_y, 'V')
                # print(wall_x, wall_y, file=sys.stderr)
                if not any(wall.isCross(w) for w in walls):
                    graph_temp = deepcopy(graph)
                    graph_temp[(wall_x, wall_y)].remove((wall_x-1, wall_y))
                    graph_temp[(wall_x-1, wall_y)].remove((wall_x, wall_y))
                    graph_temp[(wall_x, wall_y+1)].remove((wall_x-1, wall_y+1))
                    graph_temp[(wall_x-1, wall_y+1)].remove((wall_x, wall_y+1)) 
                    # check score
                    my_score = my_player.score(graph_temp)
                    if best_cost - my_score == 0:
                        op_score = sum([op.score(graph_temp) for op in op_players])
                        simulate_walls.append((op_score, wall))
        if len(simulate_walls) > 0:
            # print(simulate_walls, file=sys.stderr)
            best_wall = sorted(simulate_walls, key=lambda x:x[0])[-1][1]
            print(best_wall.x, best_wall.y, best_wall.orientation)
            return
    
    print(getDiraction((my_player.x, my_player.y), best_path[1]))
    return
    
    
players = []
walls = []

for id in range(player_count):
    players.append(Player(id, targets[id]))

while True: # game loop 
    for player in players:
        player.update()
        
    wall_count = int(input())  # number of walls on the board
    for _ in range(wall_count):
        wall_x, wall_y, orientation = input().split()
        wall_x = int(wall_x)
        wall_y = int(wall_y)
        wall = Wall(wall_x, wall_y, orientation)
        # print(wall, file=sys.stderr)
        if not any(w.isCross(wall) for w in walls):
            if orientation=='H':
                graph[(wall_x, wall_y)].remove((wall_x, wall_y-1))
                graph[(wall_x, wall_y-1)].remove((wall_x, wall_y))
                graph[(wall_x+1, wall_y)].remove((wall_x+1, wall_y-1))
                graph[(wall_x+1, wall_y-1)].remove((wall_x+1, wall_y))   
            elif orientation=='V':
                graph[(wall_x, wall_y)].remove((wall_x-1, wall_y))
                graph[(wall_x-1, wall_y)].remove((wall_x, wall_y))
                graph[(wall_x, wall_y+1)].remove((wall_x-1, wall_y+1))
                graph[(wall_x-1, wall_y+1)].remove((wall_x, wall_y+1))
            walls.append(wall)
    # print(walls, file=sys.stderr)
    action()

import sys
import math
import itertools
# w: width of the board
# h: height of the board
# player_count: number of players (2 or 3)
# my_id: id of my player (0 = 1st player, 1 = 2nd player, ...)
w, h, player_count, my_id = [int(i) for i in raw_input().split()]
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

def a_star_search_mix(graph, start, w):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    came_from[start] = None
    
    while not frontier.empty():
        current = frontier.get()
        
        if current[1] == w:
            break

        for next in graph.neighbors(current):
            if next not in came_from:
                priority = heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current
    
    return came_from

class Wall:
    def __init__(self, x, y, wall_orientation):
        self.x = x
        self.y = y
        self.wall_orientation = wall_orientation
    def __repr__(self):
        return str(self.x)+" "+str(self.y)+" "+str(self.wall_orientation)
    def __str__(self):
        return str(self.x)+" "+str(self.y)+" "+str(self.wall_orientation)
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.wall_orientation == other.wall_orientation

class Player:
    def __init__(self, x, y, walls_left, direction):
        self.x = x
        self.y = y
        self.walls_left = walls_left
        self.direction = direction
    def __repr__(self):
        return str(self.x)+" "+str(self.y)+" "+str(self.walls_left)+" "+str(self.direction)
    def __str__(self):
        return str(self.x)+" "+str(self.y)+" "+str(self.walls_left)+" "+str(self.direction)

class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
    
    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height
    
    def passable(self, id):
        return id not in self.walls
    
    def neighbors(self, id):
        (x, y) = id
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        if (x + y) % 2 == 0: results.reverse() # aesthetics
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results

class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return str(self.x)+" "+str(self.y)
    def __str__(self):
        return str(self.x)+" "+str(self.y)
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
        
#start_walls = list(itertools.chain.from_iterable((Wall(0,i,"V"),Wall(w,i,"V")) for i in range(0,w)))+ list(itertools.chain.from_iterable((Wall(i,0,"H"),Wall(i,h,"H")) for i in range(0,h)))
tmp_players = None

while True:
    players = []
    enemies = []
    for i in xrange(player_count):
        x, y, walls_left = [int(j) for j in raw_input().split()]
        direction = "NONE"
        if tmp_players != None:
            direction = getDiraction([tmp_players[i].x,tmp_players[i].y], [x,y])
        players.append(Player(x, y, walls_left, direction))
        if i!=my_id and x != -1 and y != -1:
            enemies.append(Player(x, y, walls_left, direction))        
    print >> sys.stderr, players
    
    walls_full=[]
    wall_count = int(raw_input())
    for i in xrange(wall_count):
        wall_x, wall_y, wall_orientation = raw_input().split()
        wall_x = int(wall_x)
        wall_y = int(wall_y)
        walls_full.append(Wall(wall_x, wall_y, wall_orientation))
    print >> sys.stderr, walls_full
    
    map1 = SquareGrid(w, h)
    map1.walls = []
    #for i in walls:
    a_star_search(diagram1, (1, 4), (7, 8))
    
    next_direction = ["RIGHT","UP","DOWN","LEFT"]
    print next_direction[0]
    tmp_players = players
    # action: LEFT, RIGHT, UP, DOWN or "putX putY putOrientation" to place a wall

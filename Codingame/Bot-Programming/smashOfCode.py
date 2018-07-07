import sys
import math
import random

import copy

def err(l):
    print >> sys.stderr, " ".join(str(i) for i in l)
    pass

def errLine(l):
    print >> sys.stderr, "\n".join(str(i) for i in l)
    pass

#block -1 = space, 0 = bomb, 1-5 =colors
class Stone:
    def __init__(self, color1, color2):
        self.color1 = color1
        self.color2 = color2
        # stone.rotation stone.x

width=6
height=12
group_min_size = 4
class Board:
    # changed to [col left to right][row from top to down]
    score = 0
    removed_stone = 0
    cp = -1
    cb = set()
    gb_score = 0
    grid = []

    def __init__(self):
        pass

    def drop(self, stone):
        #reset score per turn
        self.removed_stone = 0
        self.cp = -1 # cp = -1 cuz first cain not count
        self.cb = set()
        self.gb_score = 0

        if stone.rotation == 0:
            self.dropColor(stone.color1, stone.x)
            self.dropColor(stone.color2, stone.x+1)
        elif stone.rotation == 1:
            self.dropColor(stone.color1, stone.x)
            self.dropColor(stone.color2, stone.x)
        elif stone.rotation == 2:
            self.dropColor(stone.color1, stone.x)
            self.dropColor(stone.color2, stone.x-1)
        else:
            self.dropColor(stone.color2, stone.x)
            self.dropColor(stone.color1, stone.x)
        # errLine(self.grid[::-1]) # for test
        # err(["-"*20])
        self.setScore() # set score after end turn

    def dropColor(self, color, x):
        for y in range(height):
            if y+1==height or self.grid[x][y+1] != -1: # to check It's bottom
                self.grid[x][y] = color
                self.checkGroup(x, y)
                break

    def checkGroup(self, x, y):
        toRemove, color = self.checkToRemove(x, y)
        if len(toRemove) >= 4:
            self.cb.add(color)
            self.gb_score+=len(toRemove)-4
            self.cp+=1 # remove chain
            for xr, yr in toRemove:
                self.grid[xr][yr] = -1 #change color to space
                self.removed_stone += 1 # add remove stone score
            x_to_check = set() # to check that x had move
            for xr, yr in toRemove:
                self.removeStone(xr, yr)
                x_to_check.add(xr)
            movedStone = [(xm, ym) for ym in range(0,y)for xm in x_to_check if self.grid[xm][ym] != -1] # get pos stone that moved
            for mx,my in movedStone:
                self.checkGroup(mx, my)

    def checkToRemove(self, x, y):
        # check block to remove with flood fill start with x, y
        toRemove = set()
        toFill = set()
        toFill.add((x,y))
        color = copy.copy(self.grid[x][y])
        while not len(toFill)==0:
            (x,y) = toFill.pop()
            if (x,y) not in toRemove and self.grid[x][y] == color:
                toRemove.add((x,y))
                if x!=0:toFill.add((x-1,y))
                if x!=width-1:toFill.add((x+1,y))
                if y!=0:toFill.add((x,y-1))
                if y!=height-1:toFill.add((x,y+1))
        return toRemove, color

    def removeStone(self, x, y):
        self.grid[x].pop(y)
        self.grid[x].insert(0, -1)

    def setScore(self):
        cp_score = 2**(self.cp+2) if self.cp < 1 else 0
        colors_count = len(self.cb)
        cb_score = [0,2,4,8,16][colors_count-1] if colors_count else 0 # 2**(len(self.cb)-1) if len(self.cb)-1 != 0 else 0
        self.score += self.removed_stone*10*(cb_score + cp_score + self.gb_score+1)
        # err(["score :", self.removed_stone, cb_score, cp_score, self.gb_score])

    def resetScore(self):
        self.score = 0

    def setGrid(self, grid):
        self.grid = grid

loop = 0
possible_move = []
depth = 6
for r in range(4): # default 4
    if r in [1,3]:
        for x in range(1,4): # 0,6 if r = 1 or 3
            possible_move.append((x,r))
    if r==2:
        for x in range(2,4): # if r = 2 range 1,6
            possible_move.append((x,r))
    if r==0:
        for x in range(1,3): # if r = 0 range 0,5
            possible_move.append((x,r))
possible_per_turn = len(possible_move)
print "possible_per_turn: ",possible_per_turn
turns_moves_list = []
err(["possible move",possible_per_turn**depth])
for i in range(possible_per_turn**depth):
    turns_moves_list.append([possible_move[(i//(possible_per_turn**d))%possible_per_turn] for d in range(depth)])


board = Board()
def simulate(stone_list, grid, queue_of_next_move=[]):

    board.setGrid(copy.deepcopy(grid))

    max_moves = []
    max_score = -1
    
    for move_list in turns_moves_list:
        board.setGrid(copy.deepcopy(grid))
        board.resetScore()
        for d in range(depth):
            stone_list[d].x = move_list[d][0]
            stone_list[d].rotation = move_list[d][1]
            board.drop(stone_list[d])
        if board.score > max_score:
            max_score = board.score
            max_moves = move_list
            max_grid = copy.deepcopy(board.grid) #use to extract best grid
    err(["max max_moves =", max_moves])
    err(["max score =", max_score])
    return max_moves, max_grid #, max_grid

queue_of_next_move = []
grid = [[-1 for j in range(height)]for _ in range(width)]
stone_list = []
for i in xrange(7):
    color_a, color_b = [random.randint(1,5), random.randint(1,5)]
    stone_list.append(Stone(color_a, color_b))
while True:
    color_a, color_b = [random.randint(1,5), random.randint(1,5)]
    stone_list.append(Stone(color_a, color_b))
    max_moves, grid = simulate(stone_list, grid)
    queue_of_next_move = max_moves
    print queue_of_next_move[0][0], queue_of_next_move[0][1]
    stone_list.pop(0)
    queue_of_next_move.pop(0)
    loop+=1

#UP, DOWN, LEFT or RIGHT
# def getNeighbors(x,y):
#     return ((x,y+1),(x,y-1),(x-1,y),(x+1,y))

# frontier = Queue()
# frontier.put((0,0))
# came_from = {}
# came_from[(0,0)] = None

# while not frontier.empty():
#     current = frontier.get()

#     if current == goal: 
#         break           

#     for next in getNeighbors(current[0],current[1]):
#         if next not in came_from:
#             frontier.put(next)
#             came_from[next] = current
#!/usr/bin/python
import pickle
import sys

came_from_file = "came_from.txt"
current_pos_file = "current_pos_file.txt"

def getNeighbors(x,y):
    return ((x,y+1),(x,y-1),(x-1,y),(x+1,y))

def openFile(filename, data):
    try:
        with open (filename, 'rb') as fp:
            data = pickle.load(fp)
            sys.stderr.write(data)
    except:
        pass

def saveFile(filename, data):
    with open(filename, 'wb') as fp:
        pickle.dump(data, fp)

directions = ['UP', ' DOWN', ' LEFT ', 'RIGHT']
came_from = []
current_pos = (0,0)

def add_camefrom(maze, came_from, current_pos):
    for r in range(3):
        for c in range(3):
            if maze[r][c]=="#" and (current_pos[0]+c-1, current_pos[1]+r-1) not in came_from:
                came_from.append((current_pos[0]+c-1, current_pos[1]+r-1))
            elif maze[r][c]=="e":
                if c==0 and r ==1:
                    print("LEFT")
                if c==1 and r ==0:
                    print("UP")
                if c==1 and r ==2:
                    print("DOWN")
                if c==2 and r ==1:
                    print("RIGHT")
                    
def get_direction_from_current(current_pos, new_pos):
    directions = {(current_pos[0],current_pos[1]+1):"DOWN",
                 (current_pos[0],current_pos[1]-1):"UP",
                 (current_pos[0]-1,current_pos[1]):"LEFT",
                 (current_pos[0]+1,current_pos[1]):"RIGHT"}
    return directions[new_pos]
                    
def find_direction(maze, came_from, current_pos):
    for x, y in getNeighbors(current_pos[0], current_pos[1]):
        if (x,y) not in came_from:
            #sys.stderr.write(str((x,y))+", "+str(came_from))
            came_from.append((x,y))
            direction = get_direction_from_current(current_pos, (x,y))
            current_pos=(x,y)
            return direction
    # if all came from need to find not came from
            
if __name__ =="__main__":
    player = int(input())
    maze = [input() for i in range(3)]
    openFile(came_from_file, came_from)
    openFile(current_pos_file, current_pos)
    add_camefrom(maze, came_from, current_pos)
    direction = find_direction(maze, came_from, current_pos)
    saveFile(came_from_file, came_from)
    saveFile(current_pos_file, current_pos)
    sys.stderr.write("camefrom"+str(came_from))
    print(direction)
            
    
        
        

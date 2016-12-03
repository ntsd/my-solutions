import sys
import math


def lineIntersection(line1, line2):
    xdiff = (line1[0].x - line1[1].x, line2[0].x - line2[1].x)
    ydiff = (line1[0].y - line1[1].y, line2[0].y - line2[1].y) #Typo was here

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       return False

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

def lineIntersecCircle(startPos, toPos, circle, radius):
    pass
    

def pointInCircle(p1, c, radius):
    if (p1.x-c.x)**2+(p1.y-c.y)**2 < radius**2:
       return 1
    else:
       return 0
       
def getPointBetweenByLen(p1, p2, l):
    t = l/dist(p1, p2)
    x = p1.x + (p2.x-p1.x) * t
    y = p1.y + (p2.y-p1.y) * t
    return Point(x, y)

def checkBarrier(startPos, toPos, other):
     radius = other.radius + startPos.radius
     if 1:
         return True
     return False

def dist(p1, p2):
    return math.sqrt(pow(p1.x - p2.x, 2) + pow(p1.y - p2.y, 2))    

class Point(object):
    __slots__ = ['x', 'y']

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __del__(self):
        #del P destroy (delete) a point
        class_name = self.__class__.__name__

    def __add__(self, P):
        S = Point(self.x, self.y)
        S.x = self.x + P.x
        S.y = self.y + P.y
        return S

    __radd__ = __add__

    def __sub__(self, P):
        R = Point(self.x, self.y)
        R.x = self.x - P.x
        R.y = self.y - P.y
        return R

    __rsub__ = __sub__

    def __mul__(self, num):
        M = Point(self.x, self.y)
        M.x = num * self.x
        M.y = num * self.y
        return M

    __rmul__ = __mul__

    def __pow__(self, n):
        P = Point(self.x, self.y)
        P.x = self.x ** n
        P.y = self.y ** n
        return P

    def __neg__(self):
        O = Point(self.x, self.y)
        O.x = - self.x
        O.y = - self.y
        return O

    def __invert__(self):
        I = Point(self.x, self.y)
        I.x = 1. / self.x
        I.y = 1 / self.y
        return I

    def dist(self, P):
        return math.sqrt(pow(self.x - P.x, 2) + pow(self.y - P.y, 2))

    def pto_medio(self, P):
        Q = Point(self.x, self.y)
        R = (1. / 2.) * (P + Q)
        return R

    def traslacion(self, tx, ty):
        T = Point(self.x, self.y)
        T.x = self.x + tx
        T.y = self.y + ty
        return T

    def incentro(self, B, C):
        A = Point(self.x, self.y)
        a = B.dist(B)
        b = A.dist(C)
        c = A.dist(B)
        sumd = a + b + c
        A = (a / sumd) * A + (b / sumd) * B + (c / sumd) * C
        return A

    def rect2pol(self):
        P = Point(self.x, self.y)
        P.x = hypot(self.x, self.y)
        P.y = atan2(self.y, self.x)
        return(P)

    def pol2rect(self):
        P = Point(self.x, self.y)
        P.x = self.x * cos(self.y)
        P.y = self.x * sin(self.y)
        return(P)

    def entrada(self):
        point = raw_input('Introduce un punto:\n')
        point = point.replace('(', '')
        point = point.replace(')', '')
        l1 = point.rsplit(',')
        self.x = float(l1[0])
        self.y = float(l1[1])
        l1 = []

    def __repr__(self):
        return('({}, {})'.format(self.x, self.y))

my_team_id = int(raw_input())  # if 0 you need to score on the right of the map, if 1 you need to score on the left
goals= [Point(16000, 3750),Point(0, 3750)]
goal = goals[my_team_id]
magic = 100

class Wizard:
    def __init__(self, id, team, x, y, vx, vy, state):
        self.id = id
        self.team = team
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.state = state
        self.radius  = 400
    def __repr__(self):
        return str(self.x)+" "+str(self.y)+" "+str(self.team)
    def __str__(self):
        return str(self.x)+" "+str(self.y)+" "+str(self.team)
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Snaffle:
    def __init__(self, id, x, y, vx, vy):
        self.id = id
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius  = 150
    def __repr__(self):
        return str(self.x)+" "+str(self.y)
    def __str__(self):
        return str(self.x)+" "+str(self.y)
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y   
    def dist(self, P):
        return math.sqrt(pow(self.x - P.x, 2) + pow(self.y - P.y, 2))
        
class  Bludger:
    def __init__(self, id, x, y, vx, vy):
        self.id = id
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius  = 200
    def __repr__(self):
        return str(self.x)+" "+str(self.y)
    def __str__(self):
        return str(self.x)+" "+str(self.y)
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y   
    def dist(self, P):
        return math.sqrt(pow(self.x - P.x, 2) + pow(self.y - P.y, 2))
    def setTarget(self, target):
        self.target = target

while True:
    entities = int(raw_input())  # number of entities still in game
    myWizards = []
    enemyWizards = []
    snaffles = []
    bludgers = []
    for i in xrange(entities):
        entity_id, entity_type, x, y, vx, vy, state = raw_input().split()
        # print >> sys.stderr, (entity_id, entity_type, x, y, vx, vy, state)
        entity_id = int(entity_id)
        x = int(x)
        y = int(y)
        vx = int(vx)
        vy = int(vy)
        state = int(state)
        if entity_type == "WIZARD":
            myWizards.append(Wizard(entity_id,0,x,y,vx,vy,state))
        elif entity_type == "OPPONENT_WIZARD":
            enemyWizards.append(Wizard(entity_id,1,x,y,vx,vy,state))
        elif entity_type == "SNAFFLE":
            snaffles.append(Snaffle(entity_id,x,y,vx,vy))
        elif entity_type == "BLUDGER":
            bludgers.append(Bludger(x, y, vx, vy))
               
    for i in xrange(2):
        myWizard = myWizards[i]  
        snaffles = sorted(snaffles, key=lambda snaffle: snaffle.dist(myWizard))
        # print >> sys.stderr, snaffles
        snaffle = snaffles[0]
        if myWizard.state == 1:
            print "THROW",int(goal.x),int(goal.y),500
        elif (magic>=5):
            bludgers = sorted(bludgers, key=lambda snaffle: snaffle.dist(myWizard))
            print "OBLIVIATE", bludgers[0].id
            magic -= 5
        elif (magic>=20):
            
            magic-=20
        elif (magic>=20):
            magic-=20
        else:
            print "MOVE",snaffle.x,snaffle.y,100

import sys
import math

def sortDiraction(links, directForm):
    closetId = None
    closetDistance = 0
    for i in links:
        if i.diractFrom == directForm or closetId== None:
            closetId = i.diractTo
            closetDistance = i.distance
    return [closetId, closetDistance]

def getDistanceFromLinks(links, directForm, directTo):
    for i in links:
        if i.directForm == directForm and i.directTo == directTo:
            return distance

def findFactoryFromId(factorys, id):
    for i in factorys:
        if i.id == id:
            return i
 
class Link:
    def __init__(self, diractFrom, directTo, distance):
        self.diractFrom = diractFrom
        self.directTo = directTo
        self.distance = distance
        
    def __eq__(self, other):
        return self.diractFrom == other.diractFrom and self.diractTo == other.diractTo
    
class Factory:
    def __init__(self, id, player, troops, production):
        self.id = id
        self.player = player
        self.troops = troops
        self.production = production
        self.troopsInto = 0
    
    def __eq__(self, other):
        return self.id == other.id

class Troop:
    def __init__(self, id, player, diractFrom, directTo, number, remaining ):
        self.id = id
        self.player = player
        self.diractFrom = diractionFrom
        self.directTo = directionTo
        self.number = number
        self.remaining  = remaining
      
factory_count = int(input())  # the number of factories
link_count = int(input())  # the number of links between factories
links = []

for i in range(link_count):
    factory_1, factory_2, distance = [int(j) for j in input().split()]
    links.append(Link(factory_1, factory_2, distance))
    links.append(Link(factory_2, factory_1, distance))
    
while True:
    entity_count = int(input())  # the number of entities (e.g. factories and troops)
    myfactorys = []
    opFactorys = []
    naFactorys = []
    myTroops = []
    opTroops = []
    for i in range(entity_count):
        entity_id, entity_type, arg_1, arg_2, arg_3, arg_4, arg_5 = input().split()
        entity_id = int(entity_id)
        arg_1 = int(arg_1)
        arg_2 = int(arg_2)
        arg_3 = int(arg_3)
        arg_4 = int(arg_4)
        arg_5 = int(arg_5)
        if entity_type == "FACTORY":
            if arg_1 == "1":
                myfactorys.append(Factory(entity_id, arg_1, arg_2, arg_3))
            elif arg_1 == "-1":
                opFactorys.append(Factory(entity_id, arg_1, arg_2, arg_3))
            elif arg_1 == "0":
                naFactorys.append(Factory(entity_id, arg_1, arg_2, arg_3))
            
        elif entity_type == "TROOP":
            if arg_1 == "1":
                myTroops.append(Troop(entity_id, arg_1, arg_2, arg_3, arg_4, arg_5))
            elif arg_1 == "-1":
                opTroops.append(Troop(entity_id, arg_1, arg_2, arg_3, arg_4, arg_5))
    
    # To debug: print("Debug messages...", file=sys.stderr)
    for i in opTroops:
        myClosetId, myClosetDistance = sortDiraction(links, i.directTo)
        myClosetFactory = findFactoryFromId(myfactorys, myClosetId)
        distanceFromTroopToTarget = getDistanceFromLinks(links, i.directFrom, i.directTo)
        if i.directTo in naFactorys:
            if i.remaining+distanceFromTroopToTarget < myClosetDistance*2:
                print("MOVE "+myClosetId+" "+i.directTo+" "+(i.number+1))
        elif i.directTo in myfactorys:
            if i.remaining+distanceFromTroopToTarget < myClosetDistance*2:
                print("MOVE "+myClosetId+" "+i.directTo+" "+(i.number+1))
    for i in naFactorys:
        pass
    print("WAIT")

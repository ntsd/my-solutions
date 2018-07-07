import sys
import math

moved = 0

def printl(string):
    if moved == 0:print(string)

def closetDiraction(links, directTo, factorys, minTroops):
    closetId = None
    closetDistance = 999999
    if minTroops <= 0:
        minTroops = 0
    for i in links:
        if i.directFrom == directTo and i.directTo in factorys:
            myfactory = factorys[i.directTo]
            if myfactory.troops-5 > minTroops and i.distance < closetDistance:
                closetId = myfactory.id
                closetDistance = i.distance
        if i.directTo == directTo and i.directFrom in factorys:
            myfactory = factorys[i.directFrom]
            if myfactory.troops-5 > minTroops and i.distance < closetDistance:
                closetId = myfactory.id
                closetDistance = i.distance
    return [closetId, closetDistance]

def getDistanceFromLinks(links, directFrom, directTo):
    for i in links:
        if i.directFrom == directFrom and i.directTo == directTo:
            return distance

def findFactoryFromId(factorys, id):
    for i in factorys:
        if i == id:
            return i
 
class Link:
    def __init__(self, directFrom, directTo, distance):
        self.directFrom = directFrom
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
        try:
            return self.id == other.id 
        except:
            return self.id == other
    
    def __lt__(self, other):
        try:
            return self.troops < other.troops
        except:
            return self.troops < other
    
    def __str__(self):
        return 

class Troop:
    def __init__(self, id, player, directFrom, directTo, troops, remaining ):
        self.id = id
        self.player = player
        self.directFrom = directFrom
        self.directTo = directTo
        self.troops = troops
        self.remaining  = remaining
      
factory_count = int(input())  # the number of factories
link_count = int(input())  # the number of links between factories
links = []

for i in range(link_count):
    factory_1, factory_2, distance = [int(j) for j in input().split()]
    print(factory_1, factory_2, distance , file=sys.stderr)
    links.append(Link(factory_1, factory_2, distance))
    links.append(Link(factory_2, factory_1, distance))


    
while True:
    moved=0
    entity_count = int(input())  # the number of entities (e.g. factories and troops)
    myFactorys = {}
    opFactorys = {}
    naFactorys = {}
    myTroops = {}
    opTroops = {}
    for i in range(entity_count):
        entity_id, entity_type, arg_1, arg_2, arg_3, arg_4, arg_5 = input().split()
        entity_id = int(entity_id)
        arg_1 = int(arg_1)
        arg_2 = int(arg_2)
        arg_3 = int(arg_3)
        arg_4 = int(arg_4)
        arg_5 = int(arg_5)
        # print(entity_id, entity_type, arg_1, arg_2, arg_3, arg_4, arg_5 , file=sys.stderr)
        if entity_type == "FACTORY":
            if arg_1 == 1:
                myFactorys[entity_id] = Factory(entity_id, arg_1, arg_2, arg_3)
            elif arg_1 == -1:
                opFactorys[entity_id] = Factory(entity_id, arg_1, arg_2, arg_3)
            elif arg_1 == 0:
                naFactorys[entity_id] = Factory(entity_id, arg_1, arg_2, arg_3)
            
        elif entity_type == "TROOP":
            if arg_1 == 1:
                try:
                    myTroops[arg_3].append(Troop(entity_id, arg_1, arg_2, arg_3, arg_4, arg_5))
                except:
                    myTroops[arg_3] = []
                
            elif arg_1 == -1:
                try:
                    opTroops[arg_3].append(Troop(entity_id, arg_1, arg_2, arg_3, arg_4, arg_5))
                except:
                    opTroops[arg_3] = []
    
    for i in myTroops:
        troops = sum(j.troops for j in myTroops[i])
        if i in naFactorys:
            factoryTo = naFactorys[i]
            factoryTo.troops -= troops
        elif i in myFactorys:
            factoryTo = myFactorys[i]
            factoryTo.troops += troops
        elif i in opFactorys:
            factoryTo = opFactorys[i]
            factoryTo.troops -= troops
    
    # To debug: print("Debug messages...", file=sys.stderr)
    for i in opTroops:
        # distanceFromTroopToTarget = getDistanceFromLinks(links, i.directFrom, i.directTo)
        troops = sum(j.troops for j in opTroops[i])
        # print(troops, i, file=sys.stderr)
        if i in naFactorys:
            # print("i.directTo in naFactorys", i.directTo, file=sys.stderr)
            factoryTo = naFactorys[i]
            factoryTo.troops -= troops
            closetId, closetDistance = closetDiraction(links, i, myFactorys, troops)
            if closetId==None:continue
            closetFactory = myFactorys[closetId]
            # if closetFactory!=None and troops-factoryTo.troops < closetFactory.troops and troops-factoryTo.troops > 0:
            #     if moved==0 and closetId != None:print("MOVE",closetId,i,(troops-factoryTo.troops+4));moved = 1
        elif i in myFactorys:
            factoryTo = myFactorys[i]
            factoryTo.troops -= troops
            
    for i in opTroops:
        troops = sum(j.troops for j in opTroops[i])
        if i in myFactorys and myFactorys[i] < 0:
            closetId, closetDistance = closetDiraction(links, i, myFactorys, troops)           
            if closetId==None:continue
            closetFactory = myFactorys[closetId]
            print(closetFactory.troops, i , file=sys.stderr)
            if moved==0 and closetId != None:print("MOVE",closetId,i,(0-myFactorys[i].troops));moved = 1
    
    if moved==1:continue
    
    for i in naFactorys:
        # print("naFactorys" , file=sys.stderr)
        factory = naFactorys[i]
        if factory.production > 0:
            closetId, closetDistance = closetDiraction(links, factory.id, myFactorys, factory.troops)
            closetFactory = findFactoryFromId(myFactorys, closetId)
            if moved==0 and closetId!=None:print("MOVE "+str(closetId)+" "+str(factory.id)+" "+str(factory.troops+1));move = 1
    
    if moved==1:continue
     
    for i in sorted(opFactorys):
        i = opFactorys[i]
        if i.production > 2:
            for j in myFactorys:
                j=myFactorys[j]
                if j.troops > i.troops:
                    if moved==0:print("MOVE",j.id,i.id,str(i.troops+4))                    
    for i in sorted(opFactorys):
        i = opFactorys[i]
        if i.production > 1:
            for j in myFactorys:
                j=myFactorys[j]
                if j.troops > i.troops:
                    if moved==0:print("MOVE",j.id,i.id,str(i.troops+4))
    for i in sorted(opFactorys):
        i = opFactorys[i]
        for j in myFactorys:
            j=myFactorys[j]
            if j.troops > i.troops:
                if moved==0:print("MOVE",j.id,i.id,str(i.troops+4))
    print("WAIT")

import sys
import math
import random

class Box:
    def __init__(self, id, weight, volume):
        self.id = id
        self.weight = weight
        self.volume = volume
        self.truck = -1

class Truck:
    def __init__(self):
        self.weight = 0
        self.volume = 0


box_count = int(input())
boxes=[]
targetWeight=0

for i in range(box_count):
    weight, volume = [float(j) for j in input().split()]
    targetWeight+=weight;
    boxes.append(Box(i, volume, weight))


trucks={}
for i in range(100):
    trucks[i]=Truck()

trucks[-1]=Truck()

targetWeight/=box_count


boxes.sort(key=lambda x: x.weight)

for b in boxes:
    minDelta=10000
    minDeltaId = -1
    for t in range(100):
        delta=abs(targetWeight-(trucks[t].weight+b.weight))
        #print(delta)
        if delta<minDelta and trucks[t].volume+b.volume<=100:
            minDelta=delta
            minDeltaId=t
    # print(minDeltaId)
    b.truck=minDeltaId;
    trucks[minDeltaId].volume+=b.volume;
    trucks[minDeltaId].weight+=b.weight;

boxes.sort(key=id)

keepWorking=True

while keepWorking:
    keepWorking=False
    for aTruckId in range(100):
        for bTruckId in range(100):
            if aTruckId!=bTruckId:
                pass



print(' '.join(str(b.truck) for b in boxes))

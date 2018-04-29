import sys
import math

# 1. set site type
# 2. set priority need 
# 3 if opponent create unit build tower 
# 4 

# predict op_unit to my_qreen
# predict my_unit to op_qreen

#seed=974861136

def simulate_op_knight(op_unit, my_queen, my_tower, site):#check op knight attack our queen
    # towards((enemyQueen.location + (location - enemyQueen.location).resizedTo(3.0)), speed.toDouble() * frames)
    pass
        
    
def simulate_my_knight(my_unit, op_queen, my_knight_build):# find how many knight to build to attack op queen
    pass

class Site:
    def __init__(self, site_id, x, y, radius):
        self.site_id = site_id
        self.x = x
        self.y = y
        self.radius = radius
        self.predict_structure_type = ""
        
    def setAtt(self, gold_remain, maxMineSize, structure_type, owner, param1, param2):
        self.gold_remain = gold_remain
        self.maxMineSize = maxMineSize
        self.structure_type = structure_type
        self.owner = owner
        self.param1 = param1
        self.param2 = param2
    
    def setPredictStructure(self, structure_type):
        self.predict_structure_type = structure_type
        
    
class Unit:
    def __init__(self, x, y, owner, unit_type, health):
        self.x = x
        self.y = y

def dis(gun, target):
    return math.sqrt((target.y-gun.y)**2+(target.x-gun.x)**2)

def dis2(x, y, x2, y2):
    return math.sqrt((y2-y)**2+(x2-x)**2)

#enum
class enum_structure_type():
    none=-1
    mine=0
    tower=1
    barrack=2
    
def in_op_tower_range(obj, site):
    return any(sites[site].owner==1 \
    and sites[site].structure_type==enum_structure_type.tower and\
    sites[site].param2 > dis(obj,sites[site])\
    for site in sites)

def build():
    #print(sites.items()) https://www.codingame.com/replay/305446280
    global knight_build
    global archer_build
    global giant_build
    global tower_build
    global mine_build
    
    #check not in range of op tower
    # if in_op_tower_range(my_queen, sites):
    #     print('MOVE', start_pos[0], start_pos[1])
    #     return
    
    need='TOWER'
    if mine_build < 1:
        need='MINE'
    elif knight_build < 1:
        need='BARRACKS-KNIGHT'
    elif tower_build < 4:
        need='TOWER'
    elif mine_build < 5:
        need='MINE'
    elif tower_build < 5:
        need='TOWER'
    #print(loop, file=sys.stderr)
    if loop>150:
        sorted_closet_site = sorted(sites, key=lambda x: dis(my_queen, sites[x]))
        for site in sorted_closet_site:
            this_site = sites[site]
            if this_site.predict_structure_type == enum_structure_type.mine\
            and this_site.structure_type != enum_structure_type.barrack:
                print("BUILD {} {}".format(site, 'BARRACKS-KNIGHT'))
                return
    
    sorted_closet_site = sorted(sites, key=lambda x: dis(my_queen, sites[x]))
    for site in sorted_closet_site:
        this_site = sites[site]
        if in_op_tower_range(this_site, sites):
            continue
        if this_site.owner==0:
            if this_site.structure_type == enum_structure_type.mine:
                if this_site.param1 < this_site.maxMineSize:
                    print("BUILD {} {}".format(site, 'MINE'))
                    return
                
            if this_site.structure_type == enum_structure_type.tower:
                if this_site.param1 < 700:#700
                    print("BUILD {} {}".format(site, 'TOWER'))
                    return
        if this_site.owner==-1:
            if need == 'BARRACKS-KNIGHT':
                if this_site.predict_structure_type == enum_structure_type.tower:
                    print("BUILD {} {}".format(site, 'BARRACKS-KNIGHT'))
                    return
            if need == 'MINE':
                if this_site.predict_structure_type == enum_structure_type.mine:
                    if this_site.gold_remain > 0:
                        print("BUILD {} {}".format(site, 'MINE'))
                        return
                    else:
                        print("BUILD {} {}".format(site, 'BARRACKS-KNIGHT'))
                        return
            if need == 'TOWER':
                if this_site.predict_structure_type == enum_structure_type.tower:
                    print("BUILD {} {}".format(site, 'TOWER'))
                    return
        
    
    #run
    print('MOVE', start_pos[0], start_pos[1])
    
def train():
    global gold
    id_to_train = []
    if loop>60 and loop<150:
        print('TRAIN')
        return
    for site in sites:
        if sites[site].owner == 0:
            if sites[site].structure_type == 2 and sites[site].param2==0 and gold>=80 and 1:
                id_to_train.append(site)
                gold-=80
            if sites[site].structure_type == 2 and sites[site].param2==1 and gold>=100 and 0:
                id_to_train.append(site)
                gold-=100
            if sites[site].structure_type == 2 and sites[site].param2==2 and gold>=140 and 0:
                id_to_train.append(site)
                gold-=140
    if len(id_to_train)>0:
        print('TRAIN', ' '.join(map(str,id_to_train)))
    else:
        print('TRAIN')

num_sites = int(input())
sites = {}
for i in range(num_sites):
    site_id, x, y, radius = [int(j) for j in input().split()]
    sites[site_id] = Site(site_id, x, y, radius)

my_queen = None
op_queen = None
gold=0
knight_build=0
archer_build=0
giant_build=0
tower_build=0
mine_build=0
start_pos=(0,0)

my_tower=[]
my_knight_build=[]
my_mine_build=[]
op_tower=[]
op_knight_build=[]

op_creeps=[]

loop=0
while True:
    # touched_site: -1 if none
    gold, touched_site = [int(i) for i in input().split()]
    knight_build=0
    archer_build=0
    giant_build=0
    tower_build=0
    mine_build=0
    
    
    my_tower=[]
    my_knight_build=[]
    my_mine_build=[]
    op_tower=[]
    op_knight_build=[]
    for i in range(num_sites):
        # ignore_1: used in future leagues
        # ignore_2: used in future leagues
        # structure_type: -1 = No structure, 2 = Barracks
        # owner: -1 = No structure, 0 = Friendly, 1 = Enemy
        site_id, gold_remain, maxMineSize, structure_type, owner, param1, param2 = [int(j) for j in input().split()]
        sites[site_id].setAtt(gold_remain, maxMineSize, structure_type, owner, param1, param2)
        #creep type: 0 for KNIGHT, 1 for ARCHER, 2 for GIANT
        if param2 == 0 and owner==0:
            knight_build+=1
            my_knight_build.append(sites[site_id])
        if param2 == 0 and owner==1:
            op_knight_build.append(sites[site_id])
        if structure_type==enum_structure_type.mine and owner==0:
            mine_build+=1
            my_mine_build.append(sites[site_id])
        if param2 == 1 and owner==0:
            archer_build+=1
        if param2 == 2 and owner==0:
            giant_build+=1
        if structure_type == enum_structure_type.tower and owner==0:
            tower_build+=1
            my_tower.append(sites[site_id])
        if structure_type == enum_structure_type.tower and owner==1:
            op_tower.append(sites[site_id])
        
    num_units = int(input())
    
    op_creeps=[]
    for i in range(num_units):
        # unit_type: -1 = QUEEN, 0 = KNIGHT, 1 = ARCHER
        x, y, owner, unit_type, health = [int(j) for j in input().split()]
        if unit_type == -1:
            if owner == 0:
                my_queen=Unit(x, y, owner, unit_type, health)
            if owner == 1:
                op_queen=Unit(x, y, owner, unit_type, health)
        if unit_type == 0 and owner==1:
            op_creeps.append(Unit(x, y, owner, unit_type, health))
    
    
    if loop==0:#set predict structure
        sorted_closet_site = sorted(sites, key=lambda x: dis2(my_queen.x, my_queen.x, sites[x].x, my_queen.y))# dis2(my_queen.x, 500, sites[x].x, sites[x].y))
        predict_mine=0
        predict_knight=0
        predict_tower=0
        start_pos = (my_queen.x, my_queen.y)
        
        for site in sorted_closet_site:
            this_site = sites[site]
            if predict_mine<4:
                this_site.setPredictStructure(enum_structure_type.mine)
                predict_mine+=1
                continue
            this_site.setPredictStructure(enum_structure_type.tower)
    build()
    train()
    loop+=1

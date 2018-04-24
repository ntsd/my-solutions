import sys
import math

class Site:
    def __init__(self, site_id, x, y, radius):
        self.site_id = site_id
        self.x = x
        self.y = y
        self.radius = radius
        self.predict_structure_type = []
        
    def setAtt(self, gold_remain, maxMineSize, structure_type, owner, param1, param2):
        self.gold_remain = gold_remain
        self.maxMineSize = maxMineSize
        self.structure_type = structure_type
        self.owner = owner
        self.param1 = param1
        self.param2 = param2
    
    def setPredictStructure(self, structure_type):
        self.predict_structure_type.append(structure_type)
        
    
class Unit:
    def __init__(self, x, y, owner, unit_type, health):
        self.x = x
        self.y = y

def dis(gun, target):
    return math.sqrt((target.y-gun.y)**2+(target.x-gun.x)**2)

#enum
class enum_structure_type():
    none=-1
    mine=0
    tower=1
    barrack=2

def build():
    #print(sites.items())
    global knight_build
    global archer_build
    global giant_build
    sorted_closet_site = sorted(sites, key=lambda x: dis(my_queen, sites[x]))
    lowest_hp_tower = None
    lowest_hp_tower_num = float('inf')
    
    #run away from op creeps
    run_mode = 0
    for creep in op_creeps:
        if dis(my_queen, creep) < 100:
            run_mode=1

    for site in sorted_closet_site:
        this_site = sites[site]
        if this_site.structure_type == -1:
            if mine_build < 1 and this_site.gold_remain > 0 :
                print("BUILD {} {}".format(site, 'MINE'))
                return
            if knight_build < 1:
                print("BUILD {} BARRACKS-{}".format(site, 'KNIGHT'))
                return
            if tower_build < 2:
                print("BUILD {} {}".format(site, 'TOWER'))
                return
            if mine_build < 2 and this_site.gold_remain > 0 :
                print("BUILD {} {}".format(site, 'MINE'))
                return
            if tower_build < 3:
                print("BUILD {} {}".format(site, 'TOWER'))
                return
            if mine_build < 5 and this_site.gold_remain > 0 :
                print("BUILD {} {}".format(site, 'MINE'))
                return
            if tower_build < 5:
                print("BUILD {} {}".format(site, 'TOWER'))
                return
            print("BUILD {} {}".format(site, 'TOWER'))
            return
            # if archer_build==0:
            #     print("BUILD {} BARRACKS-{}".format(site, 'ARCHER'))
            #     return
            # if giant_build==0:
            #     print("BUILD {} BARRACKS-{}".format(site, 'GIANT'))
            #     return
            # if dis(my_queen, this_site) < 300 or run_mode == 0:
            #     print("BUILD {} {}".format(site, 'TOWER'))
            #     return
        #print(this_site.param1,this_site.maxMineSize, this_site.structure_type,enum_structure_type.mine ,file=sys.stderr)
        if this_site.owner==0:
            if this_site.structure_type == enum_structure_type.mine:
                if this_site.param1 < this_site.maxMineSize:
                    print("BUILD {} {}".format(site, 'MINE'))
                    return
                
            if this_site.structure_type == enum_structure_type.tower:
                if mine_build < 5 and this_site.gold_remain > 0 and tower_build > 4:
                    print("BUILD {} {}".format(site, 'MINE'))
                    return
                if this_site.param1 < 500:
                    print("BUILD {} {}".format(site, 'TOWER'))
                    return
        
        if this_site.owner==0 and this_site.structure_type == enum_structure_type.tower and this_site.param1 < lowest_hp_tower_num:
            lowest_hp_tower=this_site
            lowest_hp_tower_num=this_site.param1
    #run
    
    print('MOVE', lowest_hp_tower.x, lowest_hp_tower.y)
    
def train():
    global gold
    id_to_train = []
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
op_creeps=[]
mine_build = 0

loop=0
while True:
    # touched_site: -1 if none
    gold, touched_site = [int(i) for i in input().split()]
    knight_build=0
    archer_build=0
    giant_build=0
    tower_build=0
    mine_build = 0
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
        if structure_type==enum_structure_type.mine and owner==0:
            mine_build+=1
        archer_build+=1
        giant_build+=1
        if param2 == 1 and owner==0:
            archer_build+=1
        if param2 == 2 and owner==0:
            giant_build+=1
        if structure_type == enum_structure_type.tower and owner==0:
            tower_build+=1
        
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
        sorted_closet_site = sorted(sites, key=lambda x: dis(my_queen, sites[x]))
        predict_mine=0
        predict_knight=0
        predict_tower=0
        for site in sorted_closet_site:
            this_site = sites[site]
            if predict_mine<3:
                this_site.setPredictStructure('MINE')
                this_site.setPredictStructure('TOWER')
                predict_mine+=1
                continue
            if predict_knight<1:
                this_site.setPredictStructure('KNIGHT')
                predict_knight+=1
                continue
            this_site.setPredictStructure('TOWER')
            this_site.setPredictStructure('MINE')
    build()
    train()
    loop+=1

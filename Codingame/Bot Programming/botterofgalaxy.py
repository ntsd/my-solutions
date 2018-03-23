import sys
import math
import numpy as np
# Made with love by AntiSquid, Illedan and Wildum.
# You can help children learn to code while you participate by donating to CoderDojo.
log = sys.stderr

class Item:
    def __init__(self, item_name, item_cost, damage, health, max_health, mana, max_mana, move_speed, mana_regeneration, is_potion):
        self.item_name = item_name
        self.item_cost = item_cost
        self.damage = damage
        self.health = health
        self.max_health = max_health
        self.mana = mana
        self.max_mana = max_mana
        self.move_speed = move_speed
        self.mana_regeneration = mana_regeneration
        self.is_potion = is_potion
    def __repr__(self):
        return('(item_name:{}, item_cost:{}, damage:{}, mana_regeneration:{})'.format(self.item_name, self.item_cost, self.damage, self.mana_regeneration))
        
        
class Unit:
    def __init__(self, unit_id, team, unit_type, x, y, attack_range, health, max_health, shield, attack_damage, movement_speed, stun_duration, gold_value, count_down_1, count_down_2, count_down_3, mana, max_mana, mana_regeneration, hero_type, is_visible, items_owned):
        self.x = x
        self.y = y
        self.unit_id = unit_id
        self.team = team
        self.unit_type = unit_type
        self.attack_range = attack_range
        self.health = health
        self.max_health =  max_health
        self.shield =  shield
        self.attack_damage =  attack_damage
        self.movement_speed =  movement_speed
        self.stun_duration =  stun_duration
        self.gold_value =  gold_value
        self.count_down_1 =  count_down_1
        self.count_down_2 =  count_down_2
        self.count_down_3 =  count_down_3
        self.mana =  mana
        self.max_mana =  max_mana
        self.mana_regeneration =  mana_regeneration
        self.hero_type =  hero_type
        self.is_visible =  is_visible
        self.items_owned =  items_owned
    def __repr__(self):
        return('(id:{} hp:{}, attack:{}, range:{}, speed:{})'.format(self.unit_id, self.health, self.attack_damage, self.attack_range, self.movement_speed))


my_team = int(input()) #team 0 = left team 1 = right
bush_and_spawn = []
bush_and_spawn_point_count = int(input())  # usefrul from wood1, represents the number of bushes and the number of places where neutral units can spawn
for i in range(bush_and_spawn_point_count):
    # entity_type: BUSH, from wood1 it can also be SPAWN
    entity_type, x, y, radius = input().split()
    x = int(x)
    y = int(y)
    radius = int(radius)
    bush_and_spawn.append([x,y,radius])
print(bush_and_spawn, file=sys.stderr)
item_count = int(input())  # useful from wood2

items = []
potions = []
for i in range(item_count):
    # item_name: contains keywords such as BRONZE, SILVER and BLADE, BOOTS connected by "_" to help you sort easier
    # item_cost: BRONZE items have lowest cost, the most expensive items are LEGENDARY
    # damage: keyword BLADE is present if the most important item stat is damage
    # move_speed: keyword BOOTS is present if the most important item stat is moveSpeed
    # is_potion: 0 if it's not instantly consumed
    item_name, item_cost, damage, health, max_health, mana, max_mana, move_speed, mana_regeneration, is_potion = input().split()
    item_cost = int(item_cost)
    damage = int(damage)
    health = int(health)
    max_health = int(max_health)
    mana = int(mana)
    max_mana = int(max_mana)
    move_speed = int(move_speed)
    mana_regeneration = int(mana_regeneration)
    is_potion = int(is_potion)
    if is_potion:
        potions.append(Item(item_name, item_cost, damage, health, max_health, mana, max_mana, move_speed, mana_regeneration, is_potion))
    else:
        items.append(Item(item_name, item_cost, damage, health, max_health, mana, max_mana, move_speed, mana_regeneration, is_potion))
best_damage_weapons = sorted(filter(lambda x:x.damage>0, items), key=lambda x:x.item_cost/x.damage)
best_mana_regen_weapons = sorted(filter(lambda x:x.mana_regeneration>0, items), key=lambda x:x.item_cost/x.mana_regeneration)
hp_potions = sorted(filter(lambda x:x.health>0, potions), key=lambda x:x.item_cost/x.health)
mana_potions = sorted(filter(lambda x:x.mana>0, potions), key=lambda x:x.item_cost/x.mana)

print(item_count, "\n".join([str(i) for i in items]), "\n".join([str(i) for i in hp_potions]), file=sys.stderr)

def in_range(x,y,x2,y2,r):
    return ((x - x2)**2 + (y - y2)**2) <= r**2

def in_range2(gun, target):
    return ((gun.x - target.x)**2 + (gun.y - target.y)**2) <= (gun.attack_range)**2

def find_point_on_circle_by_angle(x2, y2, radius, angle):
    #https://stackoverflow.com/questions/35402609/point-on-circle-base-on-given-angle
    x = x2 + (radius * math.cos(angle))
    y = y2 + (radius * math.sin(angle))
    return x,y

def get_angle2(gun, target):#degree 
    #https://stackoverflow.com/questions/42258637/how-to-know-the-angle-between-two-points
    return math.atan2(target.y-gun.y, target.x-gun.x) #-3.14 - 3.14
    #https://stackoverflow.com/questions/31735499/calculate-angle-clockwise-between-two-points
    # ang1 = np.arctan2(*[-target.y, target.x])
    # ang2 = np.arctan2(*[-gun.y, gun.x])
    # return np.rad2deg((ang1 - ang2) % (2 * np.pi))

def get_dis2(o1, o2):
    return math.hypot(o1.x-o2.x, o1.y-o2.y)

def is_entity_front(ref, front):
    if my_team:
        return front.x <= ref.x
    else:
        return front.x >= ref.x

def action(hero):# todo เช็คก่อนว่ามีจำเป็นต้องเดินไหม ค่อยเช็คตี หรือ ดีไน
    #print(hero, file=sys.stderr)
    #chech in tower range
    #attack within 450 range, because 300 movement + 150 attack range
    global gold
    global farm_groot
    global farm_groot_unit
    
    #print(hero.hero_type, file=log)
        
                    
    if in_range(op_tower.x, op_tower.y, hero.x, hero.y, op_tower.attack_range*1.5): #not in tower range
        angle=math.pi if my_team==0 else 0 # abs(get_angle2(op_tower, hero))>math.pi/2
        #print("check tower range",get_angle2(op_tower, hero), angle, file=log)
        x, y = find_point_on_circle_by_angle(op_tower.x, op_tower.y, op_tower.attack_range*3, angle)#get_angle2(op_tower, hero))
        farm_groot = 1
        # print("MOVE", x, y, ";", "MOVE", x, y)
        # return
                
    if round_ > 225 and sum(map(lambda x:x.health,my_heroes)) > sum(map(lambda x:x.health,op_heroes)): # attack hero
        #sheild skill
        for potion in hp_potions[:1]:
            if hero.max_health - hero.health > potion.health and gold>=potion.item_cost:
                print("BUY", potion.item_name, ";", "BUY", potion.item_name)
                gold-=potion.item_cost
                return
        if hero.hero_type=="DOCTOR_STRANGE" and hero.count_down_2 == 0 and hero.mana >= 40:#shield
            shield = hero.max_mana * 0.5 + 50
            for h in my_heroes:
                #print(any([h.x > u.x, h.x < u.x][my_team] for u in op_units), file=log)
                if any([h.x > u.x, h.x < u.x][my_team] for u in op_units) and\
                in_range(hero.x,hero.y,h.x,h.y,500):
                    print('SHIELD', h.unit_id , ";", 'SHIELD', h.unit_id)
                    return
        if len(op_heroes) > 0:
            lowest_hero = min([(h.health, h) for h in op_heroes], key=lambda x:x[0])# chage to lowest hp
            if hero.hero_type=="IRONMAN" and hero.count_down_2 == 0 and hero.mana >= 76:#fireball
                if in_range(hero.x, hero.y, lowest_hero[1].x ,lowest_hero[1].y, 900):
                    damage = hero.mana * 0.2 + 55 * lowest_hero[0] / 1000
                    print("FIREBALL",lowest_hero[1].x, lowest_hero[1].y, ";","FIREBALL",lowest_hero[1].x, lowest_hero[1].y)
                    return
            print("ATTACK",lowest_hero[1].unit_id, ";","kill hero")
            return
    
    #print(farm_groot, file=log)
    if farm_groot:
        if (farm_groot_unit is None or farm_groot_unit.unit_id in map(lambda g:g.unit_id, groots))and len(groots)>2:
            if farm_groot_unit is None:
                farm_groot_unit = min(groots, key=lambda g:g.x) if my_team==0 else max(groots, key=lambda g:g.x)
            if hero.health > sum(map(lambda x:x.health,my_heroes))/2: #less hero hp tank
                print('MOVE_ATTACK', farm_groot_unit.x, farm_groot_unit.y, farm_groot_unit.unit_id , ";", 'kill groot tank', farm_groot_unit.unit_id)
            else:
                print('ATTACK', farm_groot_unit.unit_id , ";", 'kill groot', farm_groot_unit.unit_id)
            return
        else:
            farm_groot=0
            farm_groot_unit =None
        
    #if no one font
    front_unit=0
    for u in my_units:
        if is_entity_front(hero, u) and u.health>0:
            front_unit+=1
    #print(front_unit, file=log)
    if front_unit<2:
        if my_team:
            x= hero.x + hero.movement_speed
        else:
            x= hero.x - hero.movement_speed
        print("MOVE", x, hero.y, ";", "back", x, hero.y)
        return
        
    for u in op_units:# stay from op unit
        if in_range2(hero, u):
            angle=math.pi if my_team==0 else 0 #abs(get_angle2(u, hero))>math.pi/2
            #print(get_angle2(u, hero),angle, file=log)
            x, y = find_point_on_circle_by_angle(u.x, u.y, u.attack_damage+u.movement_speed, angle)#get_angle2(u, hero))
            print("MOVE_ATTACK", x, y, u.unit_id, ";", "move attack", x, y, u.unit_id)
            return
    
    #buy potion
    # if hero.health < hero.max_health/3:
    #     for potion in hp_potions:
    #         if hero.max_health - hero.health > potion.health and gold>=potion.item_cost:
    #             print("BUY", potion.item_name, ";", "BUY", potion.item_name)
    #             gold-=potion.item_cost
    #             return
    
        
    for potion in hp_potions[:1]:
        if hero.max_health - hero.health > potion.health and gold>=potion.item_cost\
        and hero.health <= sum(map(lambda h:h.health, my_heroes))/2:
            print("BUY", potion.item_name, ";", "BUY", potion.item_name)
            gold-=potion.item_cost
            return
        
    # for potion in mana_potions[:1]: # buy best mana potion
    #     if hero.max_mana - hero.mana - 40 > potion.mana and gold>=potion.item_cost and hero.hero_type=="DOCTOR_STRANGE":
    #         print("BUY", potion.item_name, ";", "BUY", potion.item_name)
    #         gold-=potion.item_cost
    #         return
    
    #sheild skill
    if hero.hero_type=="DOCTOR_STRANGE" and hero.count_down_2 == 0 and hero.mana >= 40:#shield
        shield = hero.max_mana * 0.5 + 50
        for h in my_heroes:
            #print(any([h.x > u.x, h.x < u.x][my_team] for u in op_units), file=log)
            if any([h.x > u.x, h.x < u.x][my_team] for u in op_units) and\
            in_range(hero.x,hero.y,h.x,h.y,500) and h.hero_type != "DOCTOR_STRANGE":
                print('SHIELD', h.unit_id , ";", 'SHIELD', h.unit_id)
                return
    
    if hero.hero_type=="DOCTOR_STRANGE" and hero.count_down_1 == 0 and hero.mana >= 50:#heal
        heal = hero.mana * 0.2
        if len(my_heroes)>1 and my_heroes[0].max_health - my_heroes[0].health >= heal\
        and my_heroes[1].max_health - my_heroes[1].health >= heal:
            if get_dis2(my_heroes[0], my_heroes[1]) <= 100*2: #check they close
                x=(my_heroes[0].x+my_heroes[1].x)/2
                y=(my_heroes[0].y+my_heroes[1].y)/2
                print('AOEHEAL',x ,y , ";", 'AOEHEAL',x ,y)
                return
            else:
                for h in my_heroes:
                    if h.health < h.max_health/2:
                        print('AOEHEAL', h.x, h.y , ";",'AOEHEAL', h.x, h.y)
                        return
        else:
            for h in my_heroes:
                if h.health < h.max_health/2:
                    print('AOEHEAL', h.x, h.y , ";",'AOEHEAL', h.x, h.y)
                    return
    
    
    # todo need to change last shot    
    for u in op_units: # kill unit
        if u.health <= hero.attack_damage and u.health>0 and\
        in_range(hero.x,hero.y,u.x,u.y,hero.attack_range+hero.movement_speed*0.9):
            angle=math.pi if my_team==0 else 0 
            x, y = find_point_on_circle_by_angle(u.x, u.y, u.attack_range+u.movement_speed, angle)
            print("ATTACK", u.unit_id, ";","KILL", u.unit_id)
            # print("MOVE_ATTACK", x, y, u.unit_id, ";","KILL", u.unit_id)
            return
        #if 2 hero can attack
        elif len(my_heroes)>1 and hero.hero_type=="IRONMAN" and u.health>0 and\
        u.health <= my_heroes[0].attack_damage + my_heroes[1].attack_damage and\
            in_range(my_heroes[0].x,my_heroes[0].y,u.x,u.y,my_heroes[0].attack_range+my_heroes[0].movement_speed*0.9) and\
            in_range(my_heroes[1].x,my_heroes[1].y,u.x,u.y,my_heroes[1].attack_range+my_heroes[1].movement_speed*0.9):
            angle=math.pi if my_team==0 else 0 
            x, y = find_point_on_circle_by_angle(u.x, u.y, u.attack_range, angle)
            print("ATTACK",u.unit_id, ";","both kill", u.unit_id)
            print("ATTACK",u.unit_id, ";","both kill", u.unit_id)
            # print("MOVE_ATTACK", x, y, u.unit_id, ";","both kill", u.unit_id)
            # print("MOVE_ATTACK", x, y, u.unit_id, ";","both kill", u.unit_id)
            return 1
            
    for u in my_units: # deny unit
        if u.health <= hero.attack_damage  and u.health>0\
        and in_range(hero.x,hero.y,u.x,u.y,hero.attack_range+hero.movement_speed*0.9):
            angle=math.pi if my_team==0 else 0 
            x, y = find_point_on_circle_by_angle(u.x, u.y, u.attack_range+u.movement_speed, angle)
            print("ATTACK", u.unit_id, ";","Deny", u.unit_id)
            # print("MOVE_ATTACK", x, y, u.unit_id, ";","Deny", u.unit_id)
            return
        #if 2 hero can attack
        elif len(my_heroes)>1 and hero.hero_type=="IRONMAN" and u.health>0 and\
            u.health <= my_heroes[0].attack_damage + my_heroes[1].attack_damage and\
            in_range(my_heroes[0].x,my_heroes[0].y,u.x,u.y,my_heroes[0].attack_range+my_heroes[0].movement_speed*0.9) and\
            in_range(my_heroes[1].x,my_heroes[1].y,u.x,u.y,my_heroes[1].attack_range+my_heroes[1].movement_speed*0.9):
            angle=math.pi if my_team==0 else 0 
            x, y = find_point_on_circle_by_angle(u.x, u.y, u.attack_range+u.movement_speed, angle)
            print("ATTACK", u.unit_id, ";","both Deny", u.unit_id)
            print("ATTACK", u.unit_id, ";","both Deny", u.unit_id)
            # print("MOVE_ATTACK", x, y, u.unit_id, ";","both Deny", u.unit_id)
            # print("MOVE_ATTACK", x, y, u.unit_id, ";","both Deny", u.unit_id)
            return 1
    
    # just buy damage
    if hero.items_owned<3:
        for i in best_damage_weapons:
            if gold>=i.item_cost:
                print("BUY", i.item_name, ";",)
                gold-=i.item_cost
                return
            
    #buy worth item 
    # if hero.items_owned==3:
    #     for i in best_damage_weapons[:1]:# worth on attack weapons # todo check sell
    #         if gold>=i.item_cost: # need to sort item worth
    #             print("BUY", i.item_name, ";","BUY", i.item_name)
    #             gold-=i.item_cost
    #             return
    
    if hero.hero_type=="DOCTOR_STRANGE" and hero.count_down_3 == 0 and hero.mana >= 40 and len(op_heroes)>0:#pull
        inrange_op_hero = [op_h for op_h in op_heroes if in_range(hero.x, hero.y, op_h.x ,op_h.y, 400)]
        if inrange_op_hero:
            lowest_hero = max([(h.mana_regeneration, h) for h in inrange_op_hero], key=lambda x:x[0])# chage to max mana regen
            print("PULL", lowest_hero[1].unit_id, ";","PULL", lowest_hero[1].unit_id)
            return
        
    #use skill
    if hero.hero_type=="IRONMAN" and hero.count_down_1 == 0 and hero.mana >= 16 and len(op_heroes)>0:#blink
        nearlest_op_unit = min([(get_dis2(hero,u), u) for u in op_units+op_heroes], key=lambda x:x[0])
        angle=math.pi if my_team==0 else 0
        x, y = find_point_on_circle_by_angle(nearlest_op_unit[1].x, nearlest_op_unit[1].y, hero.attack_range, angle)
        print("BLINK", x, y, ";","BLINK", x, y)
        hero.x = x
        hero.y = y
        return
    if hero.hero_type=="IRONMAN" and hero.count_down_2 == 0 and hero.mana >= 76 and len(op_heroes)>0:#fireball
        lowest_hero = min([(h.health, h) for h in op_heroes], key=lambda x:x[0])# chage to lowest hp
        if in_range(hero.x, hero.y, lowest_hero[1].x ,lowest_hero[1].y, 900):
            damage = hero.mana * 0.2 + 55 * lowest_hero[0] / 1000
            print("FIREBALL",lowest_hero[1].x, lowest_hero[1].y, ";","FIREBALL",lowest_hero[1].x, lowest_hero[1].y)
            return
        # farthest_hero = max([(get_dis2(hero,h), h) for h in op_heroes], key=lambda x:x[0])
        # if farthest_hero[0] <= 900:
        #     damage = hero.mana * 0.2 + 55 * farthest_hero[0] / 1000
        #     print("FIREBALL",farthest_hero[1].x, farthest_hero[1].y, ";","FIREBALL",farthest_hero[1].x, farthest_hero[1].y)
        #     return
        
    print("ATTACK_NEAREST UNIT", ";","ATTACK_NEAREST UNIT")

my_heroes = []
my_units = []
op_units = []
op_tower = None
farm_groot=0
farm_groot_unit=None
round_ = 0

while True:
    round_ += 1
    gold = int(input())
    enemy_gold = int(input())
    round_type = int(input())  # a positive value will show the number of heroes that await a command
    entity_count = int(input())
    my_heroes = []
    my_units = []
    op_heroes = []
    op_units = []
    groots = []
    for i in range(entity_count):
        # unit_type: UNIT, HERO, TOWER, can also be GROOT from wood1
        # shield: useful in bronze
        # stun_duration: useful in bronze
        # count_down_1: all countDown and mana variables are useful starting in bronze
        # hero_type: DEADPOOL, VALKYRIE, DOCTOR_STRANGE, HULK, IRONMAN
        # is_visible: 0 if it isn't
        # items_owned: useful from wood1
        unit_id, team, unit_type, x, y, attack_range, health, max_health, shield, attack_damage, movement_speed, stun_duration, gold_value, count_down_1, count_down_2, count_down_3, mana, max_mana, mana_regeneration, hero_type, is_visible, items_owned = input().split()
        unit_id = int(unit_id)
        team = int(team)
        x = int(x)
        y = int(y)
        attack_range = int(attack_range)
        health = int(health)
        max_health = int(max_health)
        shield = int(shield)
        attack_damage = int(attack_damage)
        movement_speed = int(movement_speed)
        stun_duration = int(stun_duration)
        gold_value = int(gold_value)
        count_down_1 = int(count_down_1)
        count_down_2 = int(count_down_2)
        count_down_3 = int(count_down_3)
        mana = int(mana)
        max_mana = int(max_mana)
        mana_regeneration = int(mana_regeneration)
        is_visible = int(is_visible)
        items_owned = int(items_owned)
        unit = Unit(unit_id, team, unit_type, x, y, attack_range, health, max_health, shield, attack_damage, movement_speed, stun_duration, gold_value, count_down_1, count_down_2, count_down_3, mana, max_mana, mana_regeneration, hero_type, is_visible, items_owned)
        if team == my_team:
            if unit_type == "HERO":
                my_heroes.append(unit)
            elif unit_type == "UNIT":
                my_units.append(unit)
        elif team == -1: #nau_units
            groots.append(unit)
        else:
            if unit_type == "TOWER":
                op_tower = unit
            elif unit_type == "HERO":
                op_heroes.append(unit)
            else:
                op_units.append(unit)
    # print("op_units", op_units, file=sys.stderr)
    #predict unit hp by only uni
    for my_unit in my_units:
        if len(op_heroes)==0:
            break
        dis, nearest = min([(get_dis2(my_unit,u), u) for u in op_units+op_heroes], key=lambda x:x[0])
        if nearest.unit_type == "UNIT" and dis <= my_unit.attack_range + my_unit.movement_speed*0.8:
            nearest.health -= my_unit.attack_damage
    # print("op_units", op_units, file=sys.stderr)
    # print("my_units", my_units, file=sys.stderr)
    for op_unit in op_units:
        if len(op_heroes)==0:
            break
        dis, nearest = min([(get_dis2(op_unit,u), u) for u in my_units+my_heroes], key=lambda x:x[0])
        if nearest.unit_type == "UNIT" and dis <= op_unit.attack_range + op_unit.movement_speed*0.8:
            nearest.health -= op_unit.attack_damage
            
    # print("my_units", my_units, file=sys.stderr)
    # print("my_heroes", my_heroes, file=sys.stderr)
    # print("round_", round_, file=sys.stderr)
    if round_type < 0:
        print('IRONMAN' if round_type==-2 else 'DOCTOR_STRANGE') # chosse hero
    else:
        for hero in my_heroes:
            both = action(hero)
            if both:
                break
    

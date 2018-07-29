import sys
import math
import copy

log=sys.stderr

class AttackRule:
    def __init__(self, sortMy, myFilter, sortOp, opFilter, rule):
        self.sortMy, self.myFilter, self.sortOp, self.opFilter, self.rule = sortMy, myFilter, sortOp, opFilter, rule

class Player:
    def __init__(self):
        self.mana_curve = [0, 7, 6, 5, 4, 3, 0, 0, 0, 0, 0, 0, 0]
    def setEnemy(self, player):
        self.op = player
    def update(self, player_health, player_mana, player_deck, player_rune):
        self.player_health, self.player_mana, self.player_deck, self.player_rune = player_health, player_mana, player_deck, player_rune
        self.hands = []
        self.boards = []
    def addHand(self, card):
        self.hands.append(card)
    def addBoard(self, card):
        self.boards.append(card)
        
    def draft(self, draft_list):
        max_value = 0
        card_no=0
        print(self.mana_curve, file=log)
        for i, card in enumerate(draft_list):
            if type(card) is Creature: #todo add item pick
                value = card.attack * card.defense
                if self.mana_curve[card.cost] > 0:
                    value += 100
                if value > max_value:
                    max_value = value
                    card_no = i
        self.mana_curve[draft_list[card_no].cost]-=1
        print('PICK', card_no)
     
    def summon(self): # to do make mana zero
        mana=self.player_mana
        action_list = []
        boards_count = len(self.boards)
        creature_on_hand = filter(lambda x: type(x) is Creature ,self.hands)
        for c in sorted(creature_on_hand, key=lambda x: x.cost, reverse=True):
            if boards_count < 6 or 1: # to do need to check summon again after trade
                if c.cost<=mana:
                    mana-=c.cost
                    action_list.append("SUMMON {}".format(c.instance_id))
                    if c.charge:
                        self.boards.append(c)
                    boards_count += 1
        return action_list
    
    
    def creatureAttack(self):
        action_list = []
        
        attack_rules=[
            # trade taunt value
            AttackRule(lambda my: -my.defense, lambda my: my.action,
            lambda op: -op.attack, lambda op: op.guard==1,
            lambda my, op: my.live and op.live==0),
            # attack taunt and survive
            AttackRule(lambda my: -my.attack, lambda my: my.action,
            lambda op: -op.attack, lambda op: op.guard==1,
            lambda my, op:  my.live),
            # attack taunt
            AttackRule(lambda my: -my.attack, lambda my: my.action,
            lambda op: -op.attack, lambda op: op.guard==1,
            lambda my, op: True),
             # trade lethal 
            AttackRule(lambda my: my.defense, lambda my: my.action,
            lambda op: -op.attack, lambda op: op.lethal==1,
            lambda my, op: op.live==0),
            # trade value
            AttackRule(lambda my: my.attack, lambda my: my.action,
            lambda op: -op.attack, lambda op: True,
            lambda my, op: my.live and op.live==0),
            # trade equal
            AttackRule(lambda my: my.attack, lambda my: my.action,
            lambda op: -op.attack, lambda op: True,
            lambda my, op: op.live==0), # and self.player_health < self.op.player_health
        ]
        
        for attack_rule in attack_rules:
            for my_c in sorted(filter(attack_rule.myFilter, self.boards), key=attack_rule.sortMy):
                for op_c in sorted(filter(attack_rule.opFilter, self.op.boards), key=attack_rule.sortOp):
                    my_c_temp = copy.deepcopy(my_c)
                    op_c_temp = copy.deepcopy(op_c)
                    my_c_temp.attackTarget(op_c_temp)
                    if attack_rule.rule(my_c_temp, op_c_temp):
                        my_c = my_c_temp
                        op_c = op_c_temp
                        action_list.append("ATTACK {} {} trade".format(my_c.instance_id, op_c.instance_id))
                        my_c.action = 0
                        if not my_c.live:
                            self.boards.remove(my_c)
                        if not op_c.live:
                            self.op.boards.remove(op_c)
                        break
        # go face
        for my_c in self.boards:
            if my_c.action:
                action_list.append("ATTACK {} {} face".format(my_c.instance_id, -1))
                my_c.action = 0

        return action_list
    
    def useItem(self):
        return []
    
    def play(self):
        action_list = []
        action_list += self.summon()
        action_list += self.useItem()
        action_list += self.creatureAttack()
        print(';'.join(action_list))

class Card:
    def __init__(self, card_number, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw):
        self.card_number, self.instance_id, self.location, self.card_type, self.cost, self.attack, self.defense, self.abilities, self.my_health_change, self.opponent_health_change, self.card_draw = card_number, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw
        self.action = 1
        self.shield = 1 if 'W' in abilities else 0
        self.lethal = 1 if 'L' in abilities else 0
        self.guard = 1 if 'G' in abilities else 0
        self.charge = 1 if 'C' in abilities else 0
        self.drain = 1 if 'D' in abilities else 0
        self.breakthrough = 1 if 'B'in abilities else 0
        self.live = 1
    def __hash__(self):
         return hash(self.instance_id)
    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and
            self.instance_id == other.instance_id
        )

class Item(Card):
    def use(self, target):
        pass

class Creature(Card):      
    def attackTarget(self, target): # attack op creature
        self.action = 0
        if self.shield: # damage to self
            self.shield = 0
        else:
            self.defense -= target.attack
            if self.defense <=0 or (target.lethal and type(target) is Creature):
                self.live = 0
        if target.shield: # damage to target
            target.shield = 0
        else:
            target.defense -= self.attack
            if target.defense <=0 or (self.lethal and type(target) is Creature):
                target.live = 0
    
my_player = Player()
op_player = Player()
my_player.setEnemy(op_player)
# op_player.setEnemy(my_player)
while True:
    player_health, player_mana, player_deck, player_rune = [int(j) for j in input().split()]
    my_player.update(player_health, player_mana, player_deck, player_rune)
    player_health, player_mana, player_deck, player_rune = [int(j) for j in input().split()]
    op_player.update(player_health, player_mana, player_deck, player_rune)
    
    opponent_hand = int(input())
    card_count = int(input())
    draft_list = []
    for i in range(card_count):
        card_number, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw = map(lambda x: int(x) if x[-1].isdigit() else x,input().split())
        if card_type!=0:
            card = Item(card_number, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw)
        else:
            card = Creature(card_number, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw)
        if my_player.player_mana==0:
            draft_list.append(card)
        elif location==0:
            my_player.addHand(card)
        elif location==1:
            my_player.addBoard(card)
        elif location==-1:
            op_player.addBoard(card)
    
    if my_player.player_mana==0:
        my_player.draft(draft_list)
    else:
        my_player.play()

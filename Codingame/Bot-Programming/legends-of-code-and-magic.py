import sys
import math

log=sys.stderr

class Player:
    def __init__(self):
        self.mana_curve = [0, 7, 6, 5, 4, 3, 0, 0, 0, 0, 0, 0, 0] # 1-6
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
        for i, c in enumerate(draft_list):
            value = c.attack * c.defense
            if self.mana_curve[c.cost] > 0:
                value += 100
            if value > max_value:
                max_value = value
                card = i
        self.mana_curve[draft_list[card_no].cost]-=1
        print('PICK', card_no)
     
    def summon(self): # to do make mana zero
        mana=self.player_mana
        action_list = []
        boards_count = len(self.boards)
        for c in sorted(self.hands, key=lambda x: x.cost, reverse=True):
            if boards_count < 6 or 1: # to do need to check summon again after trade
                if c.cost<=mana:
                    mana-=c.cost
                    action_list.append("SUMMON {}".format(c.instance_id))
                    if 'C' in c.abilities:
                        self.boards.append(c)
                    boards_count += 1
        return action_list
    
    def attack(self):
        action_list = []
        # check trade taunt value
        for my_c in sorted(self.boards, key=lambda x: x.defense, reverse=True):
            if my_c.action==0:
                continue
            for op_c in sorted(self.op.boards, key=lambda x: x.defense, reverse=True):
                if 'G' in op_c.abilities:
                    if my_c.attack >= op_c.defense and my_c.defense > op_c.attack:
                        action_list.append("ATTACK {} {}".format(my_c.instance_id, op_c.instance_id))
                        my_c.action = 0
                        if op_c.shield:
                            op_c.shield=0
                        else:
                            self.op.boards.remove(op_c)
                        break
        
        # check attack taunt
        for my_c in sorted(self.boards, key=lambda x: x.attack):
            if my_c.action==0:
                continue
            for op_c in sorted(self.op.boards, key=lambda x: x.attack, reverse=True):
                if 'G' in op_c.abilities:
                    action_list.append("ATTACK {} {}".format(my_c.instance_id, op_c.instance_id))
                    my_c.action = 0
                    op_c.defense -= my_c.attack
                    if op_c.shield:
                        op_c.shield=0
                    else:
                        if op_c.defense <= 0:
                            self.op.boards.remove(op_c)
                    break
        
        # check trade lethal 
        for my_c in sorted(self.boards, key=lambda x: x.defense, reverse=True):
            if my_c.action==0:
                continue
            for op_c in sorted(self.op.boards, key=lambda x: x.defense, reverse=True):
                if 'L' in op_c.abilities:
                    if my_c.attack >= op_c.defense and my_c.defense > op_c.attack:
                        action_list.append("ATTACK {} {}".format(my_c.instance_id, op_c.instance_id))
                        my_c.action = 0
                        if op_c.shield:
                            op_c.shield=0
                        else:
                            self.op.boards.remove(op_c)
                        break
        
        # check trade value
        for my_c in sorted(self.boards, key=lambda x: x.defense, reverse=True):
            if my_c.action==0:
                continue
            for op_c in sorted(self.op.boards, key=lambda x: x.defense, reverse=True):
                if my_c.attack >= op_c.defense and my_c.defense > op_c.attack:
                    action_list.append("ATTACK {} {}".format(my_c.instance_id, op_c.instance_id))
                    my_c.action = 0
                    if op_c.shield:
                        op_c.shield=0
                    else:
                        self.op.boards.remove(op_c)
                    break
            
        # check trade equal
        if self.player_health < self.op.player_health:
            for my_c in sorted(self.boards, key=lambda x: x.attack):
                if my_c.action==0:
                    continue
                for op_c in sorted(self.op.boards, key=lambda x: x.attack, reverse=True):
                    if my_c.attack >= op_c.defense:
                        action_list.append("ATTACK {} {}".format(my_c.instance_id, op_c.instance_id))
                        my_c.action = 0
                        if op_c.shield:
                            op_c.shield=0
                        else:
                            self.op.boards.remove(op_c)
                        break
        # go face
        for my_c in self.boards:
            if my_c.action:
                action_list.append("ATTACK {} {}".format(my_c.instance_id, -1))
                my_c.action = 0

        return action_list

    def play(self):
        action_list = []
        action_list += self.summon()
        action_list += self.attack()
        print(';'.join(action_list))

class Card:
    def __init__(self, card_number, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw):
        self.card_number, self.instance_id, self.location, self.card_type, self.cost, self.attack, self.defense, self.abilities, self.my_health_change, self.opponent_health_change, self.card_draw = card_number, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw
        self.action = 1
        self.shield = 1 if 'W' in abilities else 0
    def __hash__(self):
         return hash(self.instance_id)
    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and
            self.instance_id == other.instance_id
        )    
    
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
        card_number, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw = input().split()
        card_number = int(card_number)
        instance_id = int(instance_id)
        location = int(location)
        card_type = int(card_type)
        cost = int(cost)
        attack = int(attack)
        defense = int(defense)
        my_health_change = int(my_health_change)
        opponent_health_change = int(opponent_health_change)
        card_draw = int(card_draw)
        card = Card(card_number, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw)
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
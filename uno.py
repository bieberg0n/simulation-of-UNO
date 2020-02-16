# _*_ encoding: utf-8 _*_

# This .py file is a server for a UNO game.

import random
from utils import log


def generate_cards():
    colors = ['红', '黄', '绿', '蓝']
    # 暂时没有反转牌 , '反转'  '跳过',
    symbols = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '+2']
    # super_cards = ['黑转色', '黑+4']
    super_cards = []
    # generate a complete cards
    cards = [n + m for n in colors for m in symbols] * 2 + super_cards * 4
    return cards


class Table:
    def __init__(self):
        self.cards = generate_cards()
        self.players = {}
        self.can_do = 0
        self.last_card = ''
        self.add_num = 0

    def deliver_card(self):
        if len(self.cards) == 0:
            self.cards = generate_cards()

        num = random.randint(0, len(self.cards) - 1)
        card_selected = self.cards.pop(num)
        return card_selected

    def deliver_cards(self, n):
        return [self.deliver_card() for _ in range(n)]

    def add_player(self, name):
        if self.players.get(name):
            return

        p = Player(name, self.deliver_cards(5), self)
        self.players[name] = p

    def next_can_do(self):
        n = self.can_do + 1
        if n >= len(self.players.keys()):
            self.can_do = 0
        else:
            self.can_do = n

    def can_do_player_name(self):
        return list(self.players.keys())[self.can_do]

    def win(self):
        # for p in self.players.values():
        #     p.cards = self.deliver_cards(5)
        self.players = {}
        self.can_do = 0
        self.last_card = ''


class Player:
    def __init__(self, name, cards, table):
        self.name = name
        self.cards = cards
        self.table = table

    def draw(self):
        # 到我出牌了吗
        if self.table.can_do_player_name() != self.name:
            return False

        if self.table.add_num > 0:
            self.cards.extend(self.table.deliver_cards(self.table.add_num))
            self.table.add_num = 0
        else:
            self.cards.append(self.table.deliver_card())
        self.table.next_can_do()
        return True

    def lead(self, card):
        last_card = self.table.last_card
        # 到我出牌了吗
        if self.table.can_do_player_name() != self.name:
            return False

        # 开始+时不能出普通牌
        elif self.table.add_num > 0 and card[1] != '+':
            return False

        # 跟上一张牌相近吗
        elif last_card != '' and card[0] != last_card[0] and card[1:] != last_card[1:]:
            return False

        # 最后一张不能是功能牌
        elif len(self.cards) == 1 and card[1:] in ['+2']:
            return False

        self.cards.remove(card)
        if len(self.cards) <= 0:
            self.table.win()
        else:
            self.table.last_card = card
            if card[1:] == '+2':
                self.table.add_num += 2
            self.table.next_can_do()

        return True

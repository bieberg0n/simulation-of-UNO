# _*_ encoding: utf-8 _*_

# This .py file is a server for a UNO game.

import random


def generate_cards():
    colors = ['红', '黄', '绿', '蓝']
    symbols = ['1', '2', '3', '跳过', '4', '5', '6', '反转', '7', '8', '9', '10', '+2']
    super_cards = ['黑转色', '黑+4']
    # generate a complete cards
    cards = [n + m for n in colors for m in symbols] * 2 + super_cards * 4
    return cards


def deliver_cards(cards):
    if len(cards) == 0:
        cards = generate_cards()

    num = random.randint(0, len(cards) - 1)
    card_selected = cards.pop(num)
    return card_selected

# _*_ encoding: utf-8 _*_

# This .py file is a server for a UNO game.

import socket
import threading
import random
# from time import sleep
import queue
from utils import log


def generate_cards():
    colors = ['红', '黄', '绿', '蓝']
    symbols = ['1', '2', '3', '跳过', '4', '5', '6', '反转', '7', '8', '9', '10', '+2']
    super_cards = ['转色', '+4']
    # generate a complete cards
    cards = [n + m for n in colors for m in symbols] * 2 + super_cards * 4
    return cards


def deliver_cards(cards):
    if len(cards) == 0:
        cards = generate_cards()

    num = random.randint(0, len(cards) - 1)
    card_selected = cards.pop(num)
    return card_selected


def broadcast(self):
    qs = []
    while True:
        d = self.get()
        log(d)
        if d['cmd'] == 'add':
            qs.append(d['q'])
        elif d['cmd'] == 'broadcast':
            for q in qs:
                q.put(d['msg'])
        else:
            log('broadcast receive err cmd')


# def qget(q):
#     try:
#         return q.get_nowait()
#     except queue.Empty:
#         return None


def tcplink(sock, addr, cards, broadcaster):
    log('Accept new connect from {}...'.format(addr))

    name = ''
    hand_cards = [deliver_cards(cards) for _ in range(7)]

    data = sock.recv(1024).decode('utf-8')
    if data == 'receive':
        q = queue.Queue()
        broadcaster.put({
            'cmd': 'add',
            'q': q,
        })
        while True:
            news = q.get()
            sock.sendall((news + '\n').encode('utf-8'))

    else:
        while True:
            data = sock.recv(1024).decode('utf-8')
            if data[:2] == '名字':
                name = data[2:]
                broadcaster.put({
                    'cmd': 'broadcast',
                    'msg': data[2:] + '加入了游戏！',
                })
                send_card_in_hand(sock, hand_cards)

            elif data[:2] == '出牌':
                card = data[2:]
                hand_cards.remove(card)
                broadcaster.put({
                    'cmd': 'broadcast',
                    'msg': '{} 打出了一张 {} 。TA 手上还剩下 {} 张牌。'.format(name, card, len(hand_cards)),
                })
                send_card_in_hand(sock, hand_cards)

            elif data[:2] == '摸牌':
                card = deliver_cards(cards)
                hand_cards.append(card)
                broadcaster.put({
                    'cmd': 'broadcast',
                    'msg': '{} 抽了一张牌。TA 手上还剩下 {} 张牌。'.format(name, len(hand_cards)),
                })
                send_card_in_hand(sock, hand_cards)

            elif data == '':
                log(name + ' close.')
                return

            else:
                log(name + ' error data')


def send_card_in_hand(conn, cards):
    msg = ' '.join(cards) + '\n'
    conn.send(msg.encode())


def become_server(cards):
    s_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_connect.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    port = 9321
    s_connect.bind(('0.0.0.0', port))
    s_connect.listen(8)
    log('Listen to 127.0.0.1:{}. Waiting for connection...'.format(port))

    broadcaster = queue.Queue()
    threading.Thread(target=broadcast, args=(broadcaster,)).start()

    while True:
        sock, addr = s_connect.accept()
        threading.Thread(target=tcplink, args=(sock, addr, cards, broadcaster)).start()


def main():
    card_set = generate_cards()
    become_server(card_set)


if __name__ == '__main__':
    main()

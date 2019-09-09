# _*_ encoding: utf-8 _*_

# This .py file is a server for a UNO game.

import socket
import threading
import random
from time import sleep
import queue



def become_server():
	s_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s_connect.bind(('127.0.0.1', 9321))
	s_connect.listen(8)
	print('Waiting for connection...')
	while True:
		sock, addr = s_connect.accept()
		t = threading.Thread(target=tcplink, args=(sock, addr))
		t.start()

def tcplink(sock, addr):
	print('Accept new connect from %s:%s...' % addr)
	q = queue.Queue()
	sock.send(b'Welcome to the UNO game')
	sleep(1)
	sock.send('请输入你的玩家昵称：'.encode('utf-8'))
	while True:
		data = sock.recv(1024).decode('utf-8')
		news = q.get()
		if news:
			sock.send(news.encode('utf-8'))
		if data[0:2] == '名字':
			name = data[2:]
			q.put(data[2:] + '加入了游戏！')
			card_in_hand = []
			for n in range(0, 7):
				card_in_hand.append(deliver_cards(card_set))
			send_card_in_hand(card_in_hand)
		elif data[0:2] == '出牌':
			if type(int(data[2:])) == int:
				pass
			else:
				data[2:] = 100
			if int(data[2:]) < len(card_in_hand):
				card_pop = card_in_hand.pop(int(data[2:]))
				q.put(name + '打出了一张' + card_pop + ' 。 TA 手上还剩下 ' + str(len(card_in_hand)) + ' 张牌。')
				send_card_in_hand(card_in_hand)
			else:
				card_in_hand.append(deliver_cards(card_set))
				q.put(name + '抽了一张牌。 TA 手上还剩下 ' + str(len(card_in_hand)) + ' 张牌。')
				send_card_in_hand(card_in_hand)


def generate_cards():
	colors = ['红', '黄', '绿', '蓝']
	symbols = ['1', '2', '3', '跳过', '4', '5', '6', '反转', '7', '8', '9', '10', '+2']
	superCards = ['转色', '+4']
	# generate a complete cards
	cards = [n + m for n in colors for m in symbols] * 2 
	for n in range(0, 4):
		for e in superCards:
			cards.append(e)
	return cards

def deliver_cards(cards):
	if len(cards) == 0:
		cards = generate_cards()
	else:
		pass
	num_1 = random.randint(1, len(cards)) - 1
	card_selected = cards.pop(num_1) 
	return card_selected

def send_card_in_hand(cards):
	xuhao = []
	for n in range(0, len(cards)):
		xuhao.append(str(n+1) + '. ' + cards[n])
	mess = '你手上的牌有：' + xuhao
	sock.send(mess.encode('utf-8'))

if __name__ == '__main__':
	card_set = generate_cards()
	name = threading.local()
	card_in_hand = threading.local()
	become_server()

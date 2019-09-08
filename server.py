# _*_ encoding: utf-8 _*_

# This .py file is a server for a UNO game.

import socket
import threading
import random
from time import sleep
import queue

def generate_cards():
	Colors = ['红', '黄', '绿', '蓝']
	Symbols = ['1', '2', '3', '跳过', '4', '5', '6', '反转', '7', '8', '9', '10', '+2']
	SuperCards = ['转色', '+4']
	# generate a complete cards
	Cards = [n + m for n in Colors for m in Symbols] * 2 
	for n in range(0, 4):
		for e in SuperCards:
			Cards.append(e)
	return Cards

def deliver_cards(cards):
	if len(cards) == 0:
		cards = generate_cards()
	else:
		pass
	num_1 = random.randint(1, len(cards)) - 1
	card_selected = cards.pop(num_1) 
	return card_selected

def init_card(cards):
	init_card = deliver_cards(cards)
	while True:
		if init_card[-2:] not in ('跳过', '反转', '+2', '转色', '+4'):
			break
		else:
			cards.append(init_card)
			init_card = deliver_cards(cards)
	return init_card

def mess_1():
	# 第一类消息，播报牌局状态，主要用于进程间通信
	mess_1 = '牌局状态：现在的牌桌颜色是 ' + state[0] + ' , 牌桌符号是 ' + state[1] + ' , 下家要罚 ' + str(state[2]) + ' 张牌。\n'
	return mess_1

def mess_2(name, Card_in_hand):
	# 第二类消息，播报手牌状态，用于服务端和客户端通信
	show_cards = []
	for n in range(0, len(Card_in_hand)-1):
		show_cards.append(str(n+1) + '. ' + Card_in_hand[n] + ' 、')
	mess_2 = '手牌状态：' + name + ' ，您现在手上的牌组有 ' + show_cards + ' 。\n'
	return mess_2

def mess_3(Card_in_hand):
	# 第三类消息，播报 罚牌/摸牌，用于客户端通信、进程间通信
	if state[2] > 0:
		mess_3 = name + '选择了接受命运！他摸了 ' + str(state[2]) + ' 张牌。现在 TA 手上有' + str(len(Card_in_hand)) + ' 张牌。\n'
	elif state[2] == 0:
		mess_3 = name + '选择了接受命运！他摸了 1 张牌。现在 TA 手上有' + str(len(Card_in_hand)) + ' 张牌。\n'
	return mess_3

def mess_4(name, card_selected_2):
	# 第四类消息，播报出牌者出错的牌，用于客户端通信、进程间通信
	mess_4 = name + '出错牌啦！ TA 所出的牌是' + card_selected_2 + ' 。 TA 现在必须重出一张牌。\n'
	return mess_4

def mess_5(name, card_selected_2, Card_in_hand):
	# 第五类消息，播报出牌者出的牌，用于进程间通信
	mess_5 = name + '打出了一张 ' + card_selected_2 + ' 。 TA 手上还有' + str(len(Card_in_hand)) + ' 张牌。\n'
	return mess_5


def send_mess_1_2(name, Card_in_hand):
	mess_1 = mess_1()
	sock.send(mess_1.encode('utf-8'))
	queue.put(mess_1)
	mess_2 = mess_2(name, Card_in_hand)
	sock.send(mess_2.encode('utf-8'))

def send_mess_4(name, card_selected_2):
	mess_4 = mess_4(name, card_selected_2)
	queue.put(mess_4)
	sock.send(mess_4.encode('utf-8'))	

def send_mess_5(name, card_selected_2, Card_in_hand):
	mess_5 = mess_5(name, card_selected_2, Card_in_hand)
	queue.put(mess_5)
	sock.send(mess_5.encode('utf-8'))


def tcplink(sock, addr):
	print('Accept new connection from %s:%s ...' % addr)
	# 发送消息表示连接成功
	sock.send(b'Welcome!')
	sleep(1)
	# 生成玩家姓名
	sock.send('请输入您在本游戏中的姓名'.encode('utf-8'))
	name  = sock.recv(1024).decode('utf-8')
	# 生成玩家初始牌组
	for n in range(0, 7):
		Card_in_hand.append(deliver_cards(Card_set))
	# 发送牌局初始状态
	mess_1 = mess_1()
	sock.send(mess_1.encode('utf-8'))
	mess_2 = mess_2(name, Card_in_hand)
	sock.send(mess_2.encode('utf-8'))
	# 正式开始游戏
	while True:
		data = sock.recv(1024).decode('utf-8')
		mess_pub = queue.get()
		print(mess_pub)
		if mess_pub[0:4] == '牌局状态':
			mess_2 = mess_2(name, Card_in_hand)
			sock.send(mess_2.encode('utf-8'))
		# 牌局处理
		if data[0:3] == '出牌：':
			# 先检查是不是 42，是 42 就弃疗，直接摸牌
			lock.acquire()
			if data[3:] == 42:
				if state[2] > 0:
					for n in range(0, state[2]):
						Card_in_hand.append(deliver_cards)
					mess_3 = mess_3(Card_in_hand)
					# queue 用来在进程间通信。不知道这个用法对不对 
					queue.put(mess_3)
					# 给出牌者回报 TA 的罚牌信息
					sock.send(mess_3.encode('utf-8'))
					# 更新状态
					state[2] = 0
					# 给出牌者回报牌局状态和手牌状态
					send_mess_1_2(name, Card_in_hand)
				elif state[2] == 0:
					Card_in_hand.append(deliver_cards)
					mess_3 = mess_3(Card_in_hand)
					queue.put(mess_3)
					sock.send(mess_3.encode('utf-8'))
					send_mess_1_2(name, Card_in_hand)
			else:
				card_selected_2 = Card_in_hand[int(data[3:])]
				if state[2] > 0:
					if len(Card_in_hand) == 1: 
						for n in range(0, state[2]):
							Card_in_hand.append(deliver_cards)
						mess_3 = mess_3(Card_in_hand)
						queue.put(mess_3)
						sock.send(mess_3.encode('utf-8'))
						state[2] = 0
						send_mess_1_2(name, Card_in_hand)
					elif card_selected_2 == '+4':
						# +4 随时都能出
						Card_in_hand.remove(card_selected_2)
						state[2] += 4
						send_mess_5(name, card_selected_2, Card_in_hand)
						sock.send('请指定颜色：')
					elif card_selected_2[1:] == '+2':
						# 假设是符号相同
						if state[1] == '+2':
							Card_in_hand.remove(card_selected_2)
							# 刷新颜色
							state[0] == card_selected_2[0]
							state[2] += 2
							# 播报出牌
							# 显示出牌
							send_mess_5(name, card_selected_2, Card_in_hand)
							# 显示牌局状况
							send_mess_1_2(name, Card_in_hand)
						# 假设是颜色相同
						elif card_selected_2[0] == state[0]:
							Card_in_hand.remove(card_selected_2)
							# 刷新符号
							state[1] = card_selected_2[1:]
							state[3] += 2
							send_mess_5(name, card_selected_2, Card_in_hand)
							send_mess_1_2(name, Card_in_hand)
					elif card_selected_2[1:] == '反转':
						# 假设是符号相同
						if state[1] == '反转':
							Card_in_hand.remove(card_selected_2)
							state[0] == card_selected_2[0]
							send_mess_5(name, card_selected_2, Card_in_hand)
							send_mess_1_2(name, Card_in_hand)
						# 假设是颜色相同
						elif card_selected_2[0] == state[0]:
							Card_in_hand.remove(card_selected_2)
							# 刷新符号
							state[1] = card_selected_2[1:]
							send_mess_5(name, card_selected_2, Card_in_hand)
							send_mess_1_2(name, Card_in_hand)
					# 集中性地处理出错牌
					else:
						send_mess_4(name, card_selected_2)
						send_mess_1_2(name, Card_in_hand)
				elif state[2] == 0:
					if card_selected_2[-2:] == '+4':
						Card_in_hand.remove(card_selected_2)
						state[2] += 4
						send_mess_5(name, card_selected_2, Card_in_hand)
						sock.send('请指定颜色：')
					if not card_selected_2[0] == state[0] or card_selected_2[1:] == state[1]:
						send_mess_4(name, card_selected_2)
						send_mess_1_2(name, Card_in_hand)
					else:
						if card_selected_2[1:] == '+2':
							state[2] +=2
						else:
							pass
						Card_in_hand.remove(card_selected_2)
						state[0] = card_selected_2[0]
						state[1] = card_selected_2[1:]
						send_mess_5(name, card_selected_2, Card_in_hand)
						send_mess_1_2(name, Card_in_hand)
			lock.release()
		elif data[0:4] == '回报颜色':
			# 就更新颜色
			lock.acquire()
			state[0] = data[4]
			send_mess_1_2(name, Card_in_hand)
			lock.release


def become_server():
	setup_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	setup_con.bind(('127.0.0.1', 7800))
	setup_con.listen(8)
	while True:
		sock, addr = setup_con.accept()
		new_player = threading.Thread(target=tcplink, args=(sock, addr))
		lock = threading.Lock()
		new_player.start()

if __name__ == '__main__':
	Card_set = generate_cards()
	Card_in_hand = threading.local()
	name = threading.local()
	init_card = init_card(Card_set)
	state = []
	state.append(init_card[0])
	state.append(init_card[1:])
	state.append(0)
	become_server()

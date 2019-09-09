# _*_ encoding: utf-8 _*_

# This .py file is a client for a UNO game.

from queue import Queue
from threading import Thread
import socket
from utils import log


def print_msg(conn, msg_q):
	# while True:
	# 	data = conn.recv(1024).decode()
	buf = []
	for b in iter(lambda: conn.recv(1), b''):
		# log(b)
		if b == b'\n':
			data = b''.join(buf).decode()
			# log('data:', data)
			buf = []
			if data[0] == 's':
				log(data[1:])
			else:
				msg_q.put(data)

		else:
			buf.append(b)


def become_client():
	c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	c.connect(('127.0.0.1', 9321))

	name = '名字' + input('请输入你的玩家昵称：')
	c.sendall(name.encode())

	msg_q = Queue()
	Thread(target=print_msg, args=(c, msg_q)).start()
	# data = c.recv(1024).decode()

	while True:
		cards = msg_q.get().split(' ')
		log('当前牌：', ['{}.{}'.format(i, card) for i, card in enumerate(cards)], '摸牌输入p回车')
		n = input('')
		if n == 'p':
			c.sendall('摸牌'.encode())
			# card = msg_q.get()
			# cards.append(card)

		else:
			card = cards[int(n)]
			c.sendall('出牌{}'.format(card).encode())
	# data = c_connect.recv(1024).decode()
		# log(data)
		# if data == :
		# 	name = '名字' + input('请输入，按回车结束：')
		# 	c_connect.send(name.encode('utf-8'))

		# else:
		# 	chupai = '出牌' + input('请输入你要出的牌的序号，只有输入合适的序号才能出牌，否则会抽一张牌：')
		# 	c_connect.send(chupai.encode('utf-8'))


if __name__ == '__main__':
	become_client()

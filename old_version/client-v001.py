# _*_ encoding: utf-8 _*_

# This .py file is a client for a UNO game.

import socket
from utils import log


def become_client():
	c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	c.connect(('127.0.0.1', 9321))

	c.sendall(b'player')

	name = '名字' + input('请输入你的玩家昵称：')
	c.sendall(name.encode())

	while True:
		data = c.recv(1024).decode()
		cards = data.rstrip('\n').split(' ')
		log('当前牌：', ['{}.{}'.format(i, card) for i, card in enumerate(cards)], '摸牌输入p')
		n = input(':')
		if n == 'p':
			c.sendall('摸牌'.encode())

		else:
			card = cards[int(n)]
			c.sendall('出牌{}'.format(card).encode())


if __name__ == '__main__':
	become_client()

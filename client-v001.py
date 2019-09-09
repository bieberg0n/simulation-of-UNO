# _*_ encoding: utf-8 _*_

# This .py file is a client for a UNO game.

import socket


def become_client():
	c_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	c_connect.connect(('127.0.0.1', 9321))
	while True:
		data_1 = c_connect.recv(1024).decode('utf-8')
		print(data_1)
		if data_1 == '请输入你的玩家昵称：':
			name = '名字'+ input('请输入，按回车结束：')
			c_connect.send(name.encode('utf-8'))
		elif data_1 == 'Welcome to the UNO game':
			pass
		else:
			chupai = '出牌' + input('请输入你要出的牌的序号，只有输入合适的序号才能出牌，否则会抽一张牌：')
			c_connect.send(chupai.encode('utf-8'))

if __name__ == '__main__':
	become_client()
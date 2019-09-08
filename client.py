# _*_ encoding: utf-8 _*_

# This .py file is a client for a UNO game.

import socket

def start_statement():
	print('本 UNO 游戏仍处于初步开发阶段，诸多 bug 在所难免。如果打着打着突然宕机，还请各位不要跳起来。\n')
	print('本游戏还未加入自动轮局功能，请大家手动商量好出牌顺序。\n')


def become_client():
	setup_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	setup_socket.connect(('127.0.0.1', 7800))
	while True:
		content = setup_socket.recv(1024).decode('utf-8')
		if content == '请输入您在本游戏中的姓名':
			name = input('直接输入，按回车结束输入：')
			setup_socket.send(name.encode('utf-8'))
		elif content[0:4] == '手牌状态':
			print(content)
			while True:
				try:
					num = int(input('请输入你想打出的手牌序号，输入 42 即视为无牌可出，直接抽牌：'))
				except:
					pass
				if type(num) == int:
					break
			chupai = '出牌：' + str(num)
			setup_socket.send(chupai.encode('utf-8'))
		elif content == '请指定颜色：':
			while True:
				color = input('（红、黄、绿、蓝 任选其一），请好好输入以免游戏卡住:')
				if color in ('红', '黄', '绿', '蓝'):
					break
				else:
					print('错误。只能输入四个字中的一个字。')
			baose = '回报颜色' + color		
			setup_socket.send(baose.encode('utf-8'))
		else:
			print(content)



if __name__ == '__main__':
	become_client()

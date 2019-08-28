# _*_ encoding: utf-8 *_*_

# This program intends to be a simulation of playing UNO game.

# Model: Generate cards; Generate players; Play games; End game.

import random
from time import sleep


def generate_cards():
	Colors = ['红', '黄', '绿', '蓝']
	Symbols = ['1', '2', '3', '跳过', '4', '5', '6', '反转', '7', '8', '9', '10', '+2']
	SuperCards = ['转色', '+4']
	# generate a complete cards
	Cards = [n + m for n in Colors for m in Symbols]
	media = [n + m for n in Colors for m in Symbols]
	for e in media:
		Cards.append(e)
	for n in range(0, 4):
		for e in SuperCards:
			Cards.append(e)
	return Cards

def generate_user():
	User_A = []
	User_B = []
	User_C = []
	User_D = []
	return User_A, User_B, User_C, User_D

def deliver_cards():
	global Cards
	if len(Cards) == 0:
		Cards = generate_cards()
	else:
		pass
	num_1 = random.randint(1, len(Cards)) - 1
	card_selected = Cards.pop((num_1)) 
	return card_selected

def start():
	num_2 = random.randint(1, 7) - 1 
	while True:
		if User_A[num_2][-2:] == '转色':
			num_2 = random.randint(1, 7) - 1
		elif User_A[num_2][-2:] == '+4':
			num_2 = random.randint(1, 7) - 1
		elif User_A[num_2][-2:] == '跳过':
			num_2 = random.randint(1, 7) - 1
		elif User_A[num_2][-2:] == '反转':
			num_2 = random.randint(1, 7) - 1
		elif User_A[num_2][-2:] == '+2':
			num_2 = random.randint(1, 7) - 1
		else:
			break
	card_selected_1 = User_A[num_2]
	print('玩家 A 打出了手中的 ' + card_selected_1 + ' , TA 手中还剩下 ' + str(len(User_A) -1 ) + ' 张牌。\n')
	state = []
	state.append(User_A[num_2][0])
	state.append(User_A[num_2][1:])
	state.append(0)
	User_A.pop(num_2)
	return state

def color_update():
	Colors = ['红', '黄', '绿', '蓝']
	new_color = Colors[random.randint(1, 4) - 1]
	return new_color

def decision_making(current_user):
	card_selected_2 = []
	if state[2] > 0:
		if len(current_user) == 1:
			for n in range(0, state[2]):
				current_user.append(deliver_cards())
			state[2] = 0
		else:
			for e in current_user:
				if e[-2:] == '+4':
					card_selected_2 = e					
					state[0] = color_update()
					state[1] = '无'
					state[2] += 4
					current_user.remove(e)
					break				
				elif e[-2:] == '反转':
					if state[1] == '反转':
						card_selected_2 = e
						state[0] = e[0]
						current_user.remove(e)
						break
					elif e[0] == state[0]:
						card_selected_2 = e
						state[1] = '反转'
						current_user.remove(e)
						break
				elif e[-2:] == '+2':
					if state[1] == '+2':
						card_selected_2 = e
						state[0] = e[0]
						state[2] += 2
						current_user.remove(e)
						break
					elif e[0] == state[0]:
						card_selected_2 = e
						state[1] = '+2'
						state[2] += 2
						current_user.remove(e)
						break
			if card_selected_2 == []:
				for n in range(0, state[2]):
					current_user.append(deliver_cards())
					state[2] = 0
	else:
		for e in current_user:
			if e[-2:] == '+4':
				card_selected_2 = e					
				state[0] = color_update()
				state[1] = '无'
				state[2] += 4
				current_user.remove(e)
				break
			elif e[-2:] == '转色':
				card_selected_2 = e					
				state[0] = color_update()
				current_user.remove(e)
				break
			else:
				if e[0] == state[0]:
					card_selected_2 = e
					state[1] = e[1:]
					current_user.remove(e)
					break
				elif e[1:] == state[1]:
					card_selected_2 = e
					state[0] = e[0]
					current_user.remove(e)
					break
		if card_selected_2 == []:
			current_user.append(deliver_cards())
	if card_selected_2 == []:
		print('当前玩家无牌可打，因此必须摸牌。TA 手中还剩下 ' + str(len(current_user)) + ' 张牌。\n')
		print('现在的牌桌颜色是 ' + state[0] + ' , 牌桌符号是 ' + state[1] + ' , 下家要罚 ' + str(state[2]) + ' 张牌。\n')
	else:
		print('当前玩家打出了手中的 ' + card_selected_2 + ' , TA 手中还剩下 ' + str(len(current_user)) + ' 张牌。\n')
		print('现在的牌桌颜色是 ' + state[0] + ' , 牌桌符号是 ' + state[1] + ' , 下家要罚 ' + str(state[2]) + ' 张牌。\n')
	end_condition = len(current_user)
	return end_condition

			

if __name__ == '__main__':
	Cards = generate_cards()
	# 先生成出一副牌
	print('正在载入。' + '\n')
	print('牌组已经生成。' + '\n')
	sleep(1)
	# 然后要生成出 4 位用户
	User_A, User_B, User_C, User_D = generate_user()
	print('已经生成 4 位玩家。' + '\n')
	sleep(1)
	# 然后是开局发牌
	for n in range(0, 7):
		User_A.append(deliver_cards())
		User_B.append(deliver_cards())
		User_C.append(deliver_cards())
		User_D.append(deliver_cards())
	print('发牌已经完成。\n')
	print('现在由老 A 开始出第一张牌。\n')
	# 由 A 出第一张牌
	state = start()
	print('现在的牌桌颜色是 ' + state[0] + ' , 牌桌符号是 ' + state[1] + ' , 下家要罚 ' + str(state[2]) + ' 张牌。\n')
	print('现在轮到 B 出牌。\n')
	sleep(1)
	# 然后是游戏轮局、卡牌结算、 UNO 呼喊、 游戏结束。
	# 游戏轮局的办法会比较粗暴。
	# 卡牌结算由 state 变量来实现。
	while True:
		# 用 while 来保证除非终局，游戏将永远持续下去
		# 先让 B 出牌。
		con_1 = decision_making(User_B)
		if con_1 == 0:
			print('玩家 B 已经赢得了比赛！\n')
			break
		else:
			print('现在轮到 C 出牌。\n')
			sleep(1)
		con_2 = decision_making(User_C)
		if con_2 == 0:
			print('玩家 C 已经赢得了比赛！\n')
			break
		else:
			print('现在轮到 D 出牌。\n')
			sleep(1)
		con_3 = decision_making(User_D)
		if con_3 == 0:
			print('玩家 D 已经赢得了比赛！\n')
			break
		else:
			print('现在轮到 A 出牌。\n')
			sleep(1)
		con_4 = decision_making(User_A)
		if con_4 == 0:
			print('玩家 A 已经赢得了比赛！\n')
			break
		else:
			print('现在轮到 B 出牌。\n')
			sleep(1)

	



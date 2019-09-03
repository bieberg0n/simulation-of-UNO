# _*_ encoding: utf-8 _*_

# This .py file is a client for a UNO game.

import socket
import threading


def tcplink(sock, addr):
	print('Accept new connection from %s:%s ...' % addr)
	sock.send(b'Welcome!')
	while True:
		data = sock.recv(1024)
		if data or data.decode('utf-8') == 'exit':
			break
		else:
			sock.send(b'go on!')
	sock.close()
	print('Connection from %s:%s closed.' % addr)


def become_server():
	setup_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	setup_con.bind(('127.0.0.1', 7800))
	setup_con.listen(8)
	while True:
		sock, addr = setup_con.accept()
		new_player = threading.Thread(target=tcplink, args=(sock, addr))
		new_player.start()

if __name__ == '__main__':
	become_server()

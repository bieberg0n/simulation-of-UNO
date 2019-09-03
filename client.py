# _*_ encoding: utf-8 _*_

# This .py file is a client for a UNO game.

import socket


def become_client():
	setup_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	setup_socket.connect(('127.0.0.1', 7800))
	while True:
		content = setup_socket.recv(1024).decode('utf-8')
		if not content == 'forgive me':
			print(content)
			setup_socket.send(b'hello')
		else:
			break

if __name__ == '__main__':
	become_client()

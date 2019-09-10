# _*_ encoding: utf-8 _*_

import socket
from utils import log


def become_client():
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect(('127.0.0.1', 9321))

    c.sendall(b'receive')
    for b in iter(lambda: c.recv(1024), b''):
        log(b.decode().rstrip('\n'))


if __name__ == '__main__':
    become_client()

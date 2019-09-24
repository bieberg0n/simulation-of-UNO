#!/usr/bin/env python
from flask import Flask, send_file
from flask_socketio import SocketIO, emit
from uno import generate_cards, deliver_cards
from config import port
from utils import log

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)

cards = generate_cards()
players = {}


@app.route('/')
def index():
    return send_file('index.html')


@socketio.on('lead')
def client_msg(msg):
    name = msg['name']
    card = msg['card']
    log(name, 'lead', card)
    players[name].remove(card)
    emit('broadcast', {
        'type': 'lead',
        'name': name,
        'card': card,
        'remainCardsNum': len(players[name])
    }, broadcast=True)
    emit('push_cards', {'data': players[name]})


@socketio.on('draw')
def client_msg(msg):
    name = msg['name']
    log(name, 'draw')
    emit('broadcast', {
        'type': 'draw',
        'name': name,
    }, broadcast=True)
    players[name].append(deliver_cards(cards))
    emit('push_cards', {'data': players[name]})


@socketio.on('connect_event')
def connect(msg):
    name = msg['name']
    players[name] = [deliver_cards(cards) for _ in range(5)]
    log(name, 'join in')

    emit('broadcast', {
        'type': 'join',
        'name': name,
        'players': list(players.keys())
    }, broadcast=True)

    emit('push_cards', {'data': players[name]})


if __name__ == '__main__':
    # log('listen on 0.0.0.0:', port, '...')
    socketio.run(app, host='0.0.0.0', port=port, debug=True)

const log = function (...args) {
    console.log(...args)
}

const q = function (queryName) {
    return document.querySelector(queryName)
}

const qs = function (queryName) {
    return document.querySelectorAll(queryName)
}

const toggleClass = function (query, className) {
    const classSet = new Set(query.classList)
    log(classSet)
    if (classSet.has(className)) {
        query.classList.remove(className)
    } else {
        query.classList.add(className)
    }
}

const bindClick = function (queryName, handle) {
    const querys = qs(queryName)
    querys.forEach(q => q.addEventListener('click', handle, false))
}

const colorMap = function (colorName) {
    let map = new Map()
    map.set('红', 'red')
    map.set('绿', 'green')
    map.set('黄', 'yellow')
    map.set('蓝', 'blue')
    map.set('黑', 'black')
    return map.get(colorName)
}

const showCard = function (name, card) {
    let html = `<div class="card ${colorMap(card[0])}">${card.slice(1)}</div>`

    const divs = Array.from(qs('.player')).filter(p => p.dataset['name'] === name)
    if (divs.length === 0) {
        q('.players').insertAdjacentHTML('beforeEnd', `<div class="player" data-name="${name}">
            <div class="name">${name}</div>
            ${html}
        </div>`)

    } else {
        const div = divs[0]
        const p = div.querySelector('.card')
        if (p) {
            p.remove()
        }
        div.insertAdjacentHTML('beforeEnd', html)
    }
}

const showMsg = function (name, opName, card = '', other = '') {
    if (other !== '') {
        other = ' | ' + other
    }
    // q('.message').insertAdjacentHTML('afterBegin', `<p>${name}${opName}${card}${other}</p>`)
    let textarea = q('.message')
    textarea.value += `${new Date().toLocaleTimeString()}：${name}${opName}${card}${other}\n`
    textarea.scrollTop = textarea.scrollHeight
}

class Client {
    constructor() {
        this.socket = io.connect({transports: ['websocket']})
        this.name = ''
        this.currentLeadPlayer = ''
        this.currentCard = ''
        this.players = []

        this.socket.on('broadcast', (msg) => this.broadcastCallback(msg))

        this.socket.on('push_cards', (msg) => {
            log(msg.data)
            this.showCards(msg.data)
        })

        bindClick('#id-button-name', () => {
            this.name = q('#id-input-name').value
            this.socket.emit('connect_event', {name: this.name})

            toggleClass(q('.hide'), 'hide')
            toggleClass(q('.show'), 'hide')
        })

        bindClick('#id-button-draw', () => this.socket.emit('draw', {'name': this.name}))
    }

    showPlayers () {
        let playersDiv = q('.players')
        playersDiv.innerHTML = ''

        let playersHtml = this.players.map(p => {
            let cardHtml = ''
            if (this.currentCard) {
                let card = this.currentCard
                cardHtml = `<div class="card ${colorMap(card[0])}">${card.slice(1)}</div>`
            }

            if (this.currentLeadPlayer === p) {
                return `
                    <div class="player" data-name="${p}">
                      <div class="name">${p}</div>
                      ${cardHtml}
                    </div>
                `

            } else {
                return `<div class="player" data-name="${p}"><div class="name">${p}</div></div>`
            }
        }).join('')
        playersDiv.insertAdjacentHTML('afterBegin', playersHtml)
    }

    showCards(cards) {
        let html = cards.map(card => `<div class="clickable card ${colorMap(card[0])}" data-card="${card}">${card.slice(1)}</div>`).join('')

        let div = q('.cards')
        div.innerHTML = ''
        div.insertAdjacentHTML('beforeEnd', html)

        bindClick('.clickable', (event) => {
            let card = event.target.dataset.card
            this.socket.emit('lead', {name: this.name, card: card})
        })
    }

    broadcastCallback (msg) {
        log(msg)
        let name = msg['name']
        let type = msg['type']

        if (type === 'lead') {
            let card = msg['card']
            this.currentLeadPlayer = name
            this.currentCard = card
            let num = msg['remainCardsNum']
            let other = ''
            if (num === 1) {
                other = `${name} UNO!`
            } else if (num === 0) {
                other = `${name} 取得了胜利！`
            } else {
                other = `手上还有 ${num} 张牌`
            }
            // showCard(name, card)
            this.showPlayers()
            showMsg(name, ' 打出了', card, other)

        } else if (type === 'join') {
            let name = msg['name']
            this.players = msg['players']
            this.showPlayers()
            showMsg(name, ' 加入了')

        } else if (type === 'draw') {
            let num = msg['remainCardsNum']
            showMsg(name, ` 摸牌，手上有 ${num} 张牌`)

        } else {
            showMsg(name, msg['type'])
        }
    }
}

const main = function () {
    new Client()
}

main()

const log = function (...args) {
    console.log(...args)
}

const q = function (queryName) {
    return document.querySelector(queryName)
}

const qs = function (queryName) {
    return document.querySelectorAll(queryName)
}

const bindClick = function (queryName, handle) {
    const querys = qs(queryName)
    querys.forEach(q => q.addEventListener('click', handle, false))
}

const main = function () {
    let socket = io.connect()

    bindClick('#button-id-name', function() {
        let name = q('#input-id-name').value
        log('click', name)
        socket.emit('connect_event', {name: name})
    })

    // socket.on('connect', function () {
    //     socket.emit('connect_event', {name: 'bj'});
    // })

    socket.on('broadcast', function (msg) {
        log(msg.data)
    })

    socket.on('push_cards', function (msg) {
        log(msg.data)
    })
}

main()
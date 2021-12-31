<template>
    <div id="game-pannel"> </div>
    <!-- xvalue: <input v-model="xvalue" style="border: 1px solid black" @change="draw" type="number"/><br>
    yvalue: <input v-model="yvalue" style="border: 1px solid black" @change="draw" type="number"/><br> -->
    <!-- <input v-model="xpos" type="number" />
    <input v-model="ypos" type="number" />
    <select v-model="color">
        <option value="white">白</option>
        <option value="black">黑</option>
    </select>
    <button @click="move({x: xpos, y: ypos}, color)" style="border: 1px solid black;">落子</button> -->
</template>

<script>
import { ref, onUpdated, onMounted, watch, toRefs  } from 'vue'
import { SVG } from '@svgdotjs/svg.js'

let ws;

let gameDIV;
let gamePannel;
let cursor;

let boardSize = 400;
let selfColor;
let selfTurn;
const resolution = 1000;
const padding = 50
const lineWidth = 2
const lineInterval = (resolution - padding) / 15;
const chessRadius = lineInterval  / 1.1;
let boardMetrix = []

let chesses;
let blackFilling, whiteFilling;

function drawCenterSquare(base, centerX, centerY, length) {
    return base.rect(length, length).move(centerX - length / 2, centerY - length / 2)
}

function getPosition(x, y) {
    const xx = padding + lineInterval * (x - 1);
    const yy = padding + lineInterval * (15 - y);
    return {x: xx, y: yy}
}

function reset() {
    const gameDIV = document.getElementById('game-pannel')
    while (gameDIV.firstChild) {
        gameDIV.removeChild(gameDIV.firstChild)
    }
    drawBoard()
}

function drawBoard() {
    gamePannel = SVG().addTo('#game-pannel').size(resolution, resolution)
    gamePannel.node.style.zoom = boardSize / resolution;
    boardMetrix = []
    for (let i = 0; i < 15; i++) {
        boardMetrix.push(new Array(15).fill(0))
    }
    if (gamePannel == undefined) return;
    console.log(gamePannel)
    let board = gamePannel.group()
    cursor = gamePannel.rect(lineInterval, lineInterval).fill('none').stroke({color: 'black', width: 3})
    cursor.hide()
    chesses = gamePannel.group()

    blackFilling = chesses.gradient('radial', function(add) {
        add.stop(0, '#7f7f7f')
        add.stop(1, 'black')
    }).attr({fx : 0.25 , fy: 0.25, cx: 0.4, cy: 0.4})

    whiteFilling = chesses.gradient('radial', function(add) {
        add.stop(0, 'white')
        add.stop(0.75, '#e6e6e6')
        add.stop(1, '#ccc')
    }).attr({fx : 0.25 , fy: 0.25, cx: 0.4, cy: 0.4})

    const boardRect = board.rect(resolution, resolution).attr({fill: "#e1af70"})    
    for (let i = 0; i < 15; i++) {
        board.line(padding - lineWidth / 2, padding + lineInterval * i, resolution-padding-7*lineWidth, padding + lineInterval * i).stroke({width : lineWidth, color: "black"})
        board.line(padding + lineInterval * i, padding - lineWidth/2, padding + lineInterval * i, resolution-padding-7*lineWidth).stroke({width : lineWidth, color: "black"})
    }
    const marks = [[4, 4], [12, 4], [4, 12], [12, 12], [8, 8]]
    for (const i in marks) {
        const mark = marks[i];
        const pos = getPosition(mark[0], mark[1]);
        drawCenterSquare(board, pos.x, pos.y, 15).attr({fill: 'black'})
    }
    console.log(boardRect)
    gamePannel.node.onmousemove = (function(e) {
        if (!selfTurn) return
        const cursorPos = getCursorPosByMouse(e)
        const boardPos = getBoardPosByMouse(e)
        if (boardMetrix[boardPos.x][boardPos.y] == 0){
            cursor.show().center(cursorPos.x, cursorPos.y)
        }
        else {
            cursor.hide()
        }
    })
    gamePannel.node.onmouseleave = function(e) {
        cursor.hide()
    }

    gamePannel.node.onclick = function(e) {
        if (!selfTurn) return
        const boardPos = getBoardPosByMouse(event)
        if (boardMetrix[boardPos.x][boardPos.y] == 0) {
            send_move(boardPos.x, boardPos.y)
            selfTurn = false
        }
    }
}

function send_move(x, y) {
    ws.send(JSON.stringify({
        action: 'move',
        data: {x: x, y: y}
    }))
}

function getBoardPosByMouse(event) {
    const offsetX = (event.clientX - gameDIV.offsetLeft + window.pageXOffset) / boardSize * resolution
    const offsetY = (event.clientY - gameDIV.offsetTop + window.pageYOffset) / boardSize * resolution
    const boardX = Math.min(Math.max(Math.floor((offsetX - padding + lineInterval / 2) / lineInterval), 0), 14)
    const boardY = Math.min(Math.max(14 - Math.floor((offsetY - padding + lineInterval / 2) / lineInterval), 0), 14)
    return {x: boardX, y: boardY}
}

function getCursorPosByMouse(e) {
    const boardPos = getBoardPosByMouse(event)
    const cursorPos = getPosition(boardPos.x + 1, boardPos.y + 1)
    return cursorPos
}

function move(pos, color) {
    boardMetrix[pos.x][pos.y] = 1
    pos.x += 1
    pos.y += 1
    const boardPos = getPosition(pos.x, pos.y)
    const zoomRate = 1.3
    const chess = chesses.circle(chessRadius * zoomRate).move(boardPos.x - chessRadius * zoomRate / 2, boardPos.y - chessRadius * zoomRate / 2)
    if (color == 'white') {
        chess.fill(whiteFilling)
    }
    else {
        chess.fill(blackFilling)
    }
    chess.animate(200).attr({r: chessRadius / 2}).move(boardPos.x - chessRadius / 2, boardPos.y - chessRadius / 2)
    return chess
}

function handleMoveMsg(data) {
    const pos = data.move
    const color = data.color
    if (color != selfColor) {
        selfTurn = true
    }
    else {
        selfTurn = false
        cursor.hide()
    }
    move(pos, color)
}

function handleEndMsg(data) {
    cursor.hide()
    selfColor = 'none'
    selfTurn = false
}

export default {
    props: {
        size: {type: Number, default: 800},
        websocket: {type: Object, default: null}
    },
    setup(props) {
        boardSize = props.size;
        

        onMounted(() => {
            gameDIV = document.getElementById('game-pannel')
            drawBoard()
            console.log(props, 'props')
            // ws = new WebSocket("ws://127.0.0.1:8000/ws/gomoku/")
            // ws = props.websocket            
        })
        
        function setState(state) {
            selfColor = state.color
            selfTurn = state.turn
        } 

        watch(() => props.websocket, () => {
            console.log('???????????????/')
            ws = props.websocket
        })

        return {handleMoveMsg, handleEndMsg, setState, reset}
    },
}
</script>
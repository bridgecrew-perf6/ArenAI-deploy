<template>
    <canvas id="game-pannel" width="400" height="400" style="border:3px double #996633;"></canvas>
    123
    xvalue: <input v-model="xvalue" style="border: 1px solid black" @change="draw" type="number"/><br>
    yvalue: <input v-model="yvalue" style="border: 1px solid black" @change="draw" type="number"/><br>
</template>

<script>
import { ref, onUpdated, onMounted  } from 'vue'
import GameCenterVue from '../../../views/game-center/GameCenter.vue';

let gamePannelCanvas, gamePannelCtx;

const xvalue = ref("0");
const yvalue = ref("0");

function draw() {
    if (gamePannelCanvas == undefined) {
        gamePannelCanvas = document.getElementById('game-pannel');
        gamePannelCtx = gamePannelCanvas.getContext('2d');
    }
    // player1 = state.player1;
    // player2 = state.player2;
    gamePannelCtx.clearRect(0,0,400,400);
    console.log('drawing', xvalue.value, yvalue.value);
    gamePannelCtx.restore()
    gamePannelCtx.fillstyle = "red";
    gamePannelCtx.beginPath();
    gamePannelCtx.arc(parseFloat(xvalue.value), parseFloat(yvalue.value), 35, Math.PI * 2, false);
    gamePannelCtx.fillstyle = "red";
    gamePannelCtx.fill();
    gamePannelCtx.closePath();
}



export default {
    setup() {
        return { xvalue, yvalue, draw }
    },
}
</script>
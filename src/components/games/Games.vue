<template>

  <div class="bg-white mt-10">
    <div class="mx-auto px-4 max-w-7xl ">
      <div class="space-y-12">
        <div class="grid grid-cols-1 lg:grid-cols-2 w-full">
          <div class="mb-10">
            <component
              ref="gamePanel"
              :is="gameComponent"
              :size="500"
              :websocket="ws"
              :player="selfPlayer"
              :gameState="gameState"
            ></component>
            <div class="alert mt-3" style="width: 500px;" v-if="notify != ''">
              <div class="flex-1">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="#2196f3" class="w-6 h-6 mx-2">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>                          
                </svg> 
                <label>{{notify}}</label>
              </div>
            </div>
          </div>
          <div
            class="
              w-full
            "
          >
            <div class="card text-center shadow-2xl border mb-10">
              
            <div class="tabs grid grid-cols-2">
              <a class="tab tab-lifted" :class="[mode == 'manual' ? 'tab-active': null]" @click="mode='manual'">人机对抗</a> 
              <a class="tab tab-lifted" :class="[mode == 'bot' ? 'tab-active': null]" @click="mode='bot'">Bot 对抗</a> 
              <!-- <a class="tab tab-lifted" :class="[mode == 'match' ? 'tab-active': null]" @click="mode='match'">比赛</a> -->
            </div>

              <div class="card-body">
                <!-- <h2 class="card-title">shadow, center, padding</h2>  -->
                <!-- <p>Rerum reiciendis beatae tenetur excepturi aut pariatur est eos. Sit sit necessitatibus veritatis sed molestiae voluptates incidunt iure sapiente.</p>  -->
                <label class="label">
                <span class="label-text font-normal">选择我方玩家</span>
                </label> 
                <select class="select select-bordered w-full" v-model="selfPlayer" :disabled="gameState == 'going'">
                  <option disabled="disabled" selected="selected" :value="0">选择我方玩家</option> 
                  <option v-for="i in gameConfig.selectionNum + 1" :key="i" :value="i">{{gameConfig.playerNames[i]}}</option>
                </select> 
                
                <div v-if="mode=='bot'">
                <label class="label">
                <span class="label-text font-normal">选择Bot</span>
                </label> 
                  <select class="select select-bordered w-full" v-model="submitBotSelection" @change="updateSubmitFileList" @click="getAllBots">
                    <option v-for="bot in botsList" :key="bot.bot.id" :value="bot.bot.id">{{bot.env.name}}/{{bot.bot.name}}</option>
                    <!-- <option>telekinesis</option> 
                    <option>time travel</option> 
                    <option>invisibility</option> -->
                  </select> 
                <label class="label">
                <span class="label-text font-normal">选择执行文件</span>
                </label> 
                
                <select class="select select-bordered w-full" v-model="submitBotFileSelection">
                  <option v-for="file in botFileList" :key="file" :value="file">{{file}}</option>
                </select> 
                </div>

                <div class="justify-center card-actions">
                  <button class="btn btn-accent" v-if="!(gameState == 'going')" :disabled="mode=='manual' ? (selfPlayer==0) : mode == 'bot' ? (selfPlayer==0||submitBotFileSelection==-1||submitBotFileSelection=='') : false" @click="startMatch">开始游戏</button>
                  <button class="btn btn-error" v-if="(gameState == 'going')" @click="endMatch">结束游戏</button>
                </div>
              </div>
            </div> 
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { defineComponent, onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { SERVER_URL, WS_SERVER_URL, GAME_CONFIG_MAP } from "@/config.js";
import { showTranslucentLoading, hideLoading } from '@/utils.js'
import Gomoku from "./gomoku/Gomoku.vue";

let GAME_NAME;
let otherSubmissionIDs;

const notify = ref("");
let ws = ref(null);
let inited = false;
let gameConfig;
const gamePanel = ref(null);
const gameComponent = ref(null);

function initGomoku() {
  ws.value = new WebSocket(WS_SERVER_URL + "/gomoku/");

  function handleEnd() {
    gamePanel.value.setState({turn: false})
    gameState.value = 'end'
  }

  ws.value.onmessage = function (e) {
    console.log("Message received", e);
    const res = JSON.parse(e.data);
    console.log(gamePanel.value, "ta");
    if (res.action == "move") {
      const data = res.data;
      gamePanel.value.handleMoveMsg(data);
    } else if (res.action == "end") {
      const data = res.data;
      gamePanel.value.handleEndMsg(data);
      if (data.winner == 'white') {
        notify.value = '白方获胜';
      }
      else if (data.winner == 'black') {
        notify.value = '黑方获胜';
      }
      else if (data.winner == 'draw') {
        notify.value = '平局';
      }   
      handleEnd()
    }
    else if (res.action == 'error') {
      const data = res.data
      switch (data.exception) {
        case 'UnvalidMove': notify.value = gameConfig.playerNames[data.player] + '非法移动'; break;
        case 'unknown': notify.value = gameConfig.playerNames[data.player] + '运行错误'; break;
      }
      
      handleEnd()
    }
  };
  ws.value.onopen = function (e) {
    // createMatch();
  };

  ws.value.onclose = function(e) {
    ws.value = new WebSocket(WS_SERVER_URL + "/gomoku/");
    notify.value = '比赛过程中发生异常'
    handleEnd()
  }
}

function startGomoku() {
  if (mode.value == 'manual') {
    gamePanel.value.setState({
      player: selfPlayer.value == 1 ? 'black' : 'white',
      turn: selfPlayer.value == 1 ? true : false,
    })
  }
  else {
    gamePanel.value.setState({
      turn: false,
      player: 'none' 
    })
  }
  gamePanel.value.reset()
}

function endGomoku() {
  gamePanel.value.setState({
    turn: false
  })
}

function endMatch() {
  ws.value.send(JSON.stringify({
    'action': 'end'
  }))
  if (GAME_NAME == 'gomoku') {
    endGomoku()
  }
  gameState.value = 'end'
}

function startMatch() {
  if (selfPlayer.value == 0) return;
  const subids = []
  if (mode.value == 'manual') {
    let j = 0;
    for (let i = 0; i < gameConfig.selectionNum + 1; i++) {
      if (i == selfPlayer.value - 1) {
        subids.push('manual')
      } else {
        subids.push(otherSubmissionIDs[j])
        j += 1;
      }
    }
  }
  else if (mode.value == 'bot') {
    let j = 0;
    for (let i = 0; i < gameConfig.selectionNum + 1; i++) {
      if (i == selfPlayer.value - 1) {
        subids.push({
          botid: submitBotSelection.value,
          execPath: submitBotFileSelection.value
        })
      } else {
        subids.push(otherSubmissionIDs[j])
        j += 1;
      }
    }   
  }
  else return

  createMatch(subids)
  if (GAME_NAME == 'gomoku') {
    startGomoku()
  }
}

function createMatch(subids) {
  showTranslucentLoading('正在加载比赛')
  axios
    .post(SERVER_URL + "/api/v1/games/match", {
      subids: subids,
    })
    .then((res) => {
      hideLoading()
      const data = res.data
      if (data.code == 'success') {
        const data = res.data.data;
        ws.value.send(
          JSON.stringify({
            action: "start",
            data: {
              matchid: data.matchid,
            },
          })
        );
        gameState.value = 'going'
        notify.value = ''
      }
      else if (data.code == 'error') {
        console.log(data)
        switch(data.data.exception) {
          case 'construction': notify.value = gameConfig.playerNames[data.data.player] + '构造失败'; endMatch(); break;
        }
      }
    }, err=> {
      console.log(err)
    })
    .catch(err => {
      console.log(err)
    })
}

const mode = ref('manual')

const gameState = ref('unstart')
const selfPlayer = ref(0)

let botsList = ref([])
function getAllBots() {
  const ret = []
  axios.get(SERVER_URL + '/api/v1/botenv/all-bot')
  .then(res=> {
    console.log(res.data)
    const data = res.data
    for (const envid in data) {
      const env = data[envid]
      for (const botid in env.bots) {
        const bot = env.bots[botid]
        ret.push({env: env, bot: bot})
      } 
    }
    botsList.value = ret
  })
}
getAllBots()


const submitBotSelection = ref(-1)
const submitBotFileSelection = ref("")
let botFileList = ref([])
function updateSubmitFileList() {
  if (submitBotSelection.value == -1) {
    botFileList.value = []
    return
  }
  botFileList.value = []
  axios.get(SERVER_URL + '/api/v1/botenv/bot', {
    params: {
      botid: submitBotSelection.value
    }
  })
  .then(res => {
    const data = res.data
    botFileList.value = data.data.fileList
  })
  
}


export default defineComponent({
  setup() {
    const route = useRoute();
    GAME_NAME = route.params.gameName;
    otherSubmissionIDs = route.query.otherSubmissionIDs;
    console.log(otherSubmissionIDs);
    GAME_NAME = route.params.gameName;
    gameConfig = GAME_CONFIG_MAP[GAME_NAME];

    switch (GAME_NAME) {
      case "gomoku":
        gameComponent.value = Gomoku;
        break;
    }

    onMounted(function () {
      // console.log(gamePanel.value)
      // // gamePanel.value.test()
      let initFunc;
      switch (GAME_NAME) {
        case "gomoku":
          initFunc = initGomoku;
          break;
      }

      function tryInit() {
        if (gamePanel.value == null) {
          setTimeout(() => {
            tryInit();
          }, 100);
        } else {
          setTimeout(() => {
            initFunc();
          }, 1000);
        }
      }
      tryInit();
    });

    const navigation = [
      { name: "游戏中心", href: "/gamecenter" },
      { name: "关于", href: "/about" },
    ];

    return {
      gameComponent,
      gamePanel,
      ws,
      notify,
      navigation,
      gameConfig,
      mode,
      gameState,
      selfPlayer,
      startMatch,
      endMatch,
      submitBotSelection,
      submitBotFileSelection,
      updateSubmitFileList,
      getAllBots,
      botsList,
      botFileList
    };
  },
});
</script>

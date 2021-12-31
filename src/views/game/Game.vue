<template>
    <div class="bg-white">
    <div class="mx-auto py-12 px-4 max-w-7xl sm:px-6 lg:px-8 lg:py-12">
      <div class="text-2xl font-bold mb-5">{{gameConfig.gameTitle}}</div>
      <button class="btn btn-sm btn-info mr-4" :disabled="selectedNum != gameConfig.selectionNum" @click="startChallenge">挑战</button>
      <a class="btn btn-accent btn-sm" href="#submit-modal">提交</a>
      <div v-for="submission in submissions" :key="submission.id" class="mt-4">
        <div v-if="submission.selected == true" class="badge badge-outline">
          {{submission.user}}/{{submission.envName}}/{{submission.botName}}
        </div>
      </div>
        <div id="submit-modal" class="modal">
          <div class="modal-box">
            <label class="label">
            <span class="label-text font-normal">选择Bot</span>
            </label> 
              <select class="select select-bordered w-full" v-model="submitBotSelection" @change="updateSubmitFileList">
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
            <div class="modal-action">
              <a class="btn btn-sm btn-primary" @click="submitBot">确定</a> 
              <a class="btn btn-sm" @click="hideModal">取消</a>
            </div>
          </div>
        </div>

      <table class="table w-full mt-4">
        <thead>
          <tr><th>选择</th> <th>用户</th> <th>环境名称</th> <th>Bot名称</th> 
          <!-- <th>分数</th> -->
          </tr>
        </thead> 
        <tbody>
          <tr v-for="(submission, index) in submissions" :key="submission.id">
            <th>
              <label>
                <input type="checkbox" class="checkbox" @change="onChangeSelection(index)">
              </label>
            </th> 
            <td>
              {{submission.user}}
            </td> 
            <td>
              {{submission.envName}}
            </td> 
            <td>
              {{submission.botName}}
            </td> 
            <!-- <td>
              {{submission.score}}
            </td> -->
          </tr>
        </tbody>
      </table>

    

    </div>
  </div>
  <a id="operation" style="display:none;" href="#"> </a>
</template>

<script>
import { defineComponent, onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios'
import { SERVER_URL, GAME_CONFIG_MAP } from '@/config.js'


let GAME_NAME;


let gameConfig

const navigation = [
  { name: '游戏中心', href: '/gamecenter' },
  { name: '关于', href: '/about' },
]

const username = ref('')
axios.get(SERVER_URL + '/api/v1/auth/user')
.then(res => {
const data = res.data
username.value = data.data.username
})

function showModal(modalName) {
  const a = document.getElementById('operation')
  a.href = "#" + modalName
  a.click()
}

function hideModal() {
  const a = document.getElementById('operation')
  a.href = "#"
  a.click()
  submitBotSelection.value = -1
  submitBotFileSelection.value = ""
}

let botsList = ref([])
function getAllBots() {
  axios.get(SERVER_URL + '/api/v1/botenv/all-bot')
  .then(res=> {
    console.log(res.data)
    const data = res.data
    for (const envid in data) {
      const env = data[envid]
      for (const botid in env.bots) {
        const bot = env.bots[botid]
        botsList.value.push({env: env, bot: bot})
      } 
    }
    botsList.value = botsList.value
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

const submissions = reactive([])

const selectedNum = ref(0)
function onChangeSelection(index) {
  console.log(index, submissions)
  submissions[index].selected = !submissions[index].selected
  if (submissions[index].selected == true) {
    selectedNum.value += 1
  }
  else {
    selectedNum.value -= 1
  }
  console.log(submissions[index].selected)
}

function getSubmissions() {
  axios.get(SERVER_URL + '/api/v1/games/submission', {params: {
    gameName: gameConfig.gameName
  }})
  .then(res => {
    const data = res.data
    while (submissions.length > 0) {
      submissions.pop()
    }
    for (let i = 0; i < data.data.submissions.length; i++) {
      submissions.push(data.data.submissions[i])
    }
  })
}

function submitBot() {
  if (submitBotSelection.value == -1 || submitBotFileSelection.value == '') return
  axios.post(SERVER_URL + '/api/v1/games/submission', {
    gameName: gameConfig.gameName,
    execPath: submitBotFileSelection.value,
    botid: submitBotSelection.value
  })
  .then(res => {
    getSubmissions()
    hideModal()
    console.log(res.data)
  })
  .catch(err => {
    console.log(err)
  })
}

export default defineComponent({
    setup() {      
        const route = useRoute()
        const router = useRouter()
        GAME_NAME = route.params.gameName        
        gameConfig = GAME_CONFIG_MAP[GAME_NAME]
        getSubmissions()
        
        function startChallenge() {
          const otherSubmissionIDs = []
          for (let i = 0; i < submissions.length; i++) {
            if (submissions[i].selected == true) {
              otherSubmissionIDs.push(parseInt(submissions[i].id))
            }
          }
          console.log('pushed', otherSubmissionIDs)
          router.push({ path: '/match/' + gameConfig.gameName, query: {otherSubmissionIDs: otherSubmissionIDs}})
        }


        onMounted(() => {
          submitBotSelection.value = -1
          selectedNum.value = 0
        })

        return {
          gameConfig, 
          navigation, 
          username, 
          hideModal, 
          botsList, 
          submitBotSelection, 
          updateSubmitFileList, 
          botFileList, 
          submitBotFileSelection, 
          submissions, 
          onChangeSelection, 
          selectedNum, 
          submitBot, 
          startChallenge 
        }
    },
})
</script>

<template>
    <main class="flex-1">
        <div class="py-6">
          <div class="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
            <h1 class="text-2xl font-semibold text-gray-900">Bot 管理</h1>
          </div>
          <div class="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
            
            <div v-for="env in envList" :key="env.id" class="my-5 collapse border rounded-box border-base-300 collapse-arrow">
              <input type="checkbox"> 
              <div class="collapse-title text-xl font-medium ">
                {{ env.name }}
              </div> 
              <div class="collapse-content"> 
                <div class="card bordered bg-white mt-4" v-for="bot in env.bots" :key="bot.id">
                  <div class="card-body">
                    <h2 class="card-title">{{bot.name}} </h2> 
                    {{bot.info}}
                    <div class="justify-end card-actions">
                      <button class="btn btn-error btn-sm">删除</button>
                      <button class="btn btn-accent btn-sm" @click="downloadBot(bot.id)">下载</button>
                      <button class="btn btn-primary btn-sm" @click="showFilePicker(bot.id)">上传</button>
                    </div>
                  </div>
                </div>
                <div class="justify-end">
                  <button class="btn btn-neutral btn-sm mt-4" @click="setEnv(env.id)">设置环境</button> 
                    <div :id="'set-env-modal-' + env.id" class="modal">
                      <div class="modal-box">
                        <span> Python 包 </span>
                        <table class="table w-full table-compact mt-3">
                          <thead><tr><th>包名</th><th>版本</th><th>操作</th></tr></thead>
                          <tbody>
                            <tr v-for="pack in packages" :key="pack.name">
                              <td>{{pack.name}}</td>
                              <td>{{pack.version}}</td>
                              <td><button class="btn btn-outline btn-error btn-xs" @click="deletePackage(pack.name)">删除</button></td>
                            </tr>
                            <tr>
                              <td><input v-model="newPackageName" type="text" placeholder="包名" class="input input-xs input-bordered"></td>
                              <td><input v-model="newPackageVersion" type="text" placeholder="版本（选填）" class="input input-xs input-bordered"></td>
                              <td><button class="btn btn-outline btn-accent btn-xs" @click="addPackage(newPackageName)">添加</button></td>
                            </tr>
                          </tbody>
                        </table>
                        <!-- <div class="w-full flex">
                          <label class="label">
                            <span class="label-text">添加Python包</span>
                          </label> 
                          <input type="text" placeholder="包名" class="input input-sm input-bordered">
                          <input type="text" placeholder="版本（选填）" class="input input-sm input-bordered">
                        </div> -->
                        <div class="modal-action">
                          <a class="btn btn-sm btn-error " @click="null">删除环境</a> 
                          <a class="btn btn-sm btn-primary" @click="updatePackage(env.id)" :class="[updatingPackage ? 'loading' : null]"> {{!updatingPackage ? '确定' : '取消后仍可在后台更新'}}</a> 
                          <a class="btn btn-sm" @click="hideModal">取消</a>
                        </div>
                      </div>
                    </div>

                  <a class="btn btn-primary btn-sm mt-4 ml-4" :href="'#new-bot-modal-' + env.id">添加Bot</a> 
                    <div :id="'new-bot-modal-' + env.id" class="modal">
                      <div class="modal-box">
                        <label class="label">
                        <span class="label-text font-normal">Bot名称</span>
                        </label> 
                        <input type="text" placeholder="Bot名称" class="input input-sm input-bordered w-full" v-model="newBotName">
                        <div class="modal-action">
                          <a class="btn btn-sm btn-primary" @click="createBot(env.id)">确定</a> 
                          <a class="btn btn-sm" @click="hideModal">取消</a>
                        </div>
                      </div>
                    </div>

                </div>
              </div>
            </div> 
            <a href="#new-env-modal" class="btn btn-primary btn-sm mt-4">添加环境</a> 
              <div id="new-env-modal" class="modal">
                <div class="modal-box">
                  <label class="label">
                  <span class="label-text font-normal">环境名称</span>
                  </label> 
                  <input type="text" placeholder="环境名称" class="input input-sm input-bordered w-full" v-model="newEnvName">
                  <div class="modal-action">
                    <a class="btn btn-sm btn-primary" @click="createEnv">确定</a> 
                    <a class="btn btn-sm" @click="hideModal">取消</a>
                  </div>
                </div>
              </div>
            <!-- <button class="btn btn-primary btn-sm">添加环境</button>  -->
          </div>
        </div>
      </main>
      <a id="operation" style="display:none;" href="#"> </a>
      <div v-show="false">
        <input type="file" id="file-picker" ref="filePicker" webkitdirectory directory multiple="multiple" v-on:change="handleFileUpload" />
      </div>
</template>

<script>

import { ref, reactive, onMounted } from 'vue'
import axios from 'axios'
import { SERVER_URL } from '@/config'
import { showTranslucentLoading, hideLoading, showNotify } from '@/utils.js'

const envList = ref([])

const newEnvName = ref('')
const newBotName = ref('')
const disabled = ref(false)

function updateEnvList() {
  axios.get(SERVER_URL + '/api/v1/botenv/all-bot')
  .then(res=> {
    console.log(res.data)
      envList.value = res.data
  })
}

function showModal(modalName) {
  const a = document.getElementById('operation')
  a.href = "#" + modalName
  a.click()
}

function hideModal() {
  const a = document.getElementById('operation')
  a.href = "#"
  a.click()
  newEnvName.value = ''
  newBotName.value = ''
  newPackageName.value = ''
  newPackageVersion.value = ''
  packages.value = []
}

let fileList = []
let handlingBotID;
function handleFileUpload() {
  fileList = document.getElementById('file-picker').files;
  console.log('handling file upload', fileList)
  if (fileList.length != 0) {
    uploadBot()
  }
}

function uploadBot() {
  showTranslucentLoading('正在上传')
  const formData = new FormData()
  for (let i = 0; i < fileList.length; i++) {
    formData.append('files', fileList[i])
    formData.append('relativePath', fileList[i].webkitRelativePath)
  }
  formData.append('botid', handlingBotID)
  axios.put(SERVER_URL + '/api/v1/botenv/bot',
    formData
  )
  .then(res => {
    document.getElementById('file-picker').value = ''
    console.log(res)
    hideLoading()
    showNotify('提示', '上传成功')
  })
  .catch(err => {
    console.log(err)
    hideLoading()
    showNotify('提示', '上传失败')
  })
}

function getBotFileList(botid) {
  console.log(botid)
  axios.get(SERVER_URL + '/api/v1/botenv/bot', { params: {
    botid: botid
  }})
  .then(res => {
    console.log(res.data)
  })
}

function downloadBot(botid) {
  axios.get(SERVER_URL + '/api/v1/botenv/bot-file', {params: {
    botid: botid
  }, responseType: 'blob'})
  .then(res => {
    const data = res.data;
    let fileReader = new FileReader();
    fileReader.onload = function() {
        try {
            let jsonData = JSON.parse(this.result);  // 说明是普通对象数据，后台转换失败
        if (jsonData.code) {
            that.$message.error(jsonData.message)
        }
        } catch (err) {   // 解析成对象失败，说明是正常的文件流
            const blob = new Blob([data], {type: 'application/zip'});
            const filename = res.headers['content-disposition'];
            const downloadElement = document.createElement('a');
            const href = window.URL.createObjectURL(blob); //创建下载的链接
            downloadElement.href = href;
            [downloadElement.download] = [filename];
            document.body.appendChild(downloadElement);
            downloadElement.click(); //点击下载
            document.body.removeChild(downloadElement); //下载完成移除元素
            window.URL.revokeObjectURL(href); //释放blob对
        }
    };
    fileReader.readAsText(data)
  })
}

function showFilePicker(botid) {
  handlingBotID = botid
  document.getElementById('file-picker').click()
}

function createEnv() {
  if (newEnvName.value == '') return
  axios.post(SERVER_URL + '/api/v1/botenv/env', {
    'name': newEnvName.value
  })
  .then(res => {
    const data = res.data
    if (data.action == 'info') {
      console.log(data.data.msg)
      hideModal()
      updateEnvList()
    }
  })
  .catch(err => {
    console.log(err)
  })
}


const packages = ref([]);
function getPackages(envid) {
  console.log(envid)
  axios({
    url: SERVER_URL + '/api/v1/botenv/env',
    params: {envid: envid},
    method: 'GET'
  })
  .then(res => {
    packages.value = res.data
    console.log(res.data)
  })
  .catch((err) => {
    console.log(err)
  })
}

function deletePackage(packageName) {
  for (let i = 0; i < packages.value.length; i++) {
    const pack = packages.value[i]
    if (pack.name == packageName) {
      packages.value.splice(i, 1)
    }
  }
}

const updatingPackage = ref(false)
function updatePackage(envid) {
  updatingPackage.value = true
  axios.put(SERVER_URL + '/api/v1/botenv/env', {
    packages: packages.value,
    envid: envid
  })
  .then(res => {
    updatingPackage.value = false
    console.log('Packages updated')
    hideModal()
  })
  .catch(err => {
    console.log(err)
  })
}


const newPackageName = ref('')
const newPackageVersion = ref('')
function addPackage() {
  packages.value.push({
    name: newPackageName.value,
    version: newPackageVersion.value
  })
  newPackageName.value = ''
  newPackageVersion.value = ''
}

function setEnv(envid) {
  getPackages(envid)
  showModal('set-env-modal-' + envid);
}

function createBot(envid) {
  if (newBotName.value == '') return
  axios.post(SERVER_URL + '/api/v1/botenv/bot', {
    'name': newBotName.value,
    'envid': envid
  })
  .then(res => {
    const data = res.data;
    if (data.action == 'info') {
      console.log(data.data.msg)
      hideModal()
      updateEnvList()
    }
  })
  .catch(err => {
    console.log(err)
  })
}

export default {
    setup() {
        updateEnvList()
        
        return {
          envList,
          hideModal,
          disabled,
          newEnvName,
          newBotName,
          createEnv,
          createBot,
          getPackages,
          deletePackage,
          addPackage,
          updatePackage,
          updatingPackage,
          setEnv,
          packages,
          newPackageName,
          newPackageVersion,
          handleFileUpload,
          uploadBot,
          showFilePicker,
          getBotFileList,
          downloadBot
        }
    },
}
</script>
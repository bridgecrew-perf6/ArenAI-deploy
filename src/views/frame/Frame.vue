<script setup>

import { ref } from 'vue'
import { showLoading, hideLoading } from '@/utils.js'
import { SERVER_URL } from '@/config.js'
import { useRouter } from 'vue-router'
import axios from 'axios'

const username = ref('')
const router = useRouter()

showLoading('正在与服务器建立连接')
axios.get(SERVER_URL + '/api/v1/auth/user')
.then(res => {
    const data = res.data
    username.value = data.data.username
    // router.push('/gamecenter')
    hideLoading()
})
.catch((err) => {
    // router.push('/login')
    window.location.href = "/login"
    // console.log(err)
    hideLoading()
})

const navigation = [
  { name: '游戏中心', href: '/gamecenter' },
  { name: '关于', href: '/about' },
]

function logout() {
    axios.delete(SERVER_URL + '/api/v1/auth/token')
    .then(res => {
        const data = res.data;
        if (data.code == 'success') {
            localStorage.removeItem('Authorization')
            router.push('/login')
        }
    })
}

</script>


<template>
    <header class="bg-indigo-600">
    <nav class="max-w-7xl mx-auto px-4 sm:px-6 md:px-8" aria-label="Top">
      <div class="w-full py-6 flex items-center justify-between border-b border-indigo-500 md:border-none">
        <div class="flex items-center">
          <a href="#">
            <img class="h-10 w-auto" src="/favicon.svg" alt="" />
          </a>
          <div class="ml-10 space-x-8">
            <a v-for="link in navigation" :key="link.name" :href="link.href" class="text-base font-medium text-white hover:text-indigo-50">
              {{ link.name }}
            </a>
          </div>
        </div>
        <a class="ml-10 space-x-4 text-white">
            <div class="dropdown dropdown-end">
                <a href="#" class="avatar placeholder" tabindex="0">
                    <div class="bg-neutral-focus text-neutral-content rounded-full w-10 h-10">
                        <span>{{username[0].toUpperCase()}}</span>
                    </div>
                    <div class="mx-2">
                    {{username}}
                    </div>
                </a>
                
                <ul tabindex="0" class="p-2 mt-2 shadow menu dropdown-content bg-base-100 rounded-box w-52 text-black text-sm">
                    <li>
                    <a href="/profile">个人中心</a>
                    </li> 
                    <li>
                    <a @click="logout">注销</a>
                    </li> 
                </ul>
            </div>
          <!-- <router-link to="profile">  </router-link> -->
        </a>
      </div>
    </nav>
  </header>
  <router-view></router-view>
</template>
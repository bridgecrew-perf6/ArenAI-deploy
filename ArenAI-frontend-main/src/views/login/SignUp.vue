<template>
<div class="min-h-screen flex flex-col justify-center py-12 sm:px-6 lg:px-8 bg-blue-50">
  <div class="sm:mx-auto sm:w-full sm:max-w-md">
    <img class="mx-auto h-12 w-auto" src="/favicon.svg" alt="Workflow">
    <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900 tracking-widest">
      注册ArenAI
    </h2>
    <p class="mt-2 text-center text-sm text-gray-600">
      或
      <a to="/login" href="/login" class="font-medium text-indigo-600 hover:text-indigo-500">
        登录
      </a>
    </p>
  </div>

  <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
    <div class="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
      <form class="space-y-6" onsubmit="return false">
        <div>
          <label for="username" class="block text-sm font-medium text-gray-700">
            用户名
          </label>
          <div class="mt-1">
            <input id="username" name="username" type="text" :disabled="loginLoading" v-model="username" required class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
          </div>
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-gray-700">
            密码
          </label>
          <div class="mt-1">
            <input id="password" name="password" type="password" :disabled="loginLoading" autocomplete="current-password" v-model="password" required class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
          </div>
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-gray-700">
            确认密码
          </label>
          <div class="mt-1">
            <input id="confirm-password" name="confirm-password" type="password" :disabled="loginLoading" autocomplete="current-password" v-model="confirmPassword" required class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
          </div>
        </div>

        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <!-- <input id="remember-me" name="remember-me" type="checkbox" class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded">
            <label for="remember-me" class="ml-2 block text-sm text-gray-900">
              记住我
            </label> -->
          </div>

          <!-- <div class="text-sm">
            <a href="#" class="font-medium text-indigo-600 hover:text-indigo-500">
              忘记密码?
            </a>
          </div> -->
        </div>

        <div>
          <button @click="login" class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 btn" :class="[loginLoading ? 'loading' : null]">
            登录
          </button>
        </div>
      </form>

    </div>
  </div>
</div>
</template>

<script>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { SERVER_URL } from '@/config.js'
import { showNotify } from '@/utils.js'
import { SwitchHorizontalIcon } from '@heroicons/vue/outline'
const username = ref('')
const password = ref('')
const confirmPassword = ref('')

export default {
  setup() {
    const router = useRouter()

    const loginLoading = ref(false)

    function login() {
      if (username.value == '' || password.value == '' || confirmPassword.value == '') {
        // showNotify('提示', '请完整填写登录信息')
        return
      }
      if (password.value != confirmPassword.value) {
        showNotify('提示', '两次输入密码不一致')
        return
      }
      loginLoading.value = true;
      axios.post(SERVER_URL + '/api/v1/auth/user', {
        username: username.value,
        password: password.value
      })
      .then(res => {
        const data = res.data
        console.log(data)
        if (data.code == 'success') {
          localStorage.setItem('Authorization', data.data.token)
          router.push('/login')
        }
        else if (data.code == 'error') {
          switch(data.data.msg) {
            case 'UnvalidUserName': showNotify('提示', '用户名不合法<br>请确认用户名以应为字母开头，并由英文字母或数字组成'); break;
            case 'UnvalidPassword': showNotify('提示', '密码不合法<br>请确认密码长度为6-32位，并由英文字母、数字、\'_\'、\'.\'组成'); break;
            case 'UserExist': showNotify('提示', '用户名已存在'); break;
          }
        }
        loginLoading.value = false;
      })
      .catch(err => {
        showNotify('提示', '连接错误')
        loginLoading.value = false;
      })
    }

    return {
      username,
      password,
      confirmPassword,
      login,
      loginLoading,
    }
  },
}
</script>
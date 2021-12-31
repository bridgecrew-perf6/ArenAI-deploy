<!-- This example requires Tailwind CSS v2.0+ -->
<template>
  <!--
    This example requires updating your template:

    ```
    <html class="h-full bg-gray-100">
    <body class="h-full">
    ```
  -->
  <div>
    <TransitionRoot as="template" :show="sidebarOpen">
      <Dialog as="div" class="fixed inset-0 flex z-40 md:hidden" @close="sidebarOpen = false">
        <TransitionChild as="template" enter="transition-opacity ease-linear duration-300" enter-from="opacity-0" enter-to="opacity-100" leave="transition-opacity ease-linear duration-300" leave-from="opacity-100" leave-to="opacity-0">
          <DialogOverlay class="fixed inset-0 bg-gray-600 bg-opacity-75" />
        </TransitionChild>
        <TransitionChild as="template" enter="transition ease-in-out duration-300 transform" enter-from="-translate-x-full" enter-to="translate-x-0" leave="transition ease-in-out duration-300 transform" leave-from="translate-x-0" leave-to="-translate-x-full">
          <div class="relative flex-1 flex flex-col max-w-xs w-full bg-white">
            <TransitionChild as="template" enter="ease-in-out duration-300" enter-from="opacity-0" enter-to="opacity-100" leave="ease-in-out duration-300" leave-from="opacity-100" leave-to="opacity-0">
              <div class="absolute top-0 right-0 -mr-12 pt-2">
                <button type="button" class="ml-1 flex items-center justify-center h-10 w-10 rounded-full focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white" @click="sidebarOpen = false">
                  <span class="sr-only">Close sidebar</span>
                  <XIcon class="h-6 w-6 text-white" aria-hidden="true" />
                </button>
              </div>
            </TransitionChild>
            <div class="flex-1 h-0 pt-5 pb-4 overflow-y-auto">
              <div class="flex-shrink-0 flex items-center px-4">
                <router-link to="/gamecenter"><img class="h-8 w-auto" src="/favicon.svg" alt="Workflow" /></router-link>
                <span class="text-black font-black mx-4 text-xl"> 个人中心 </span>
              </div>
              <nav class="mt-5 px-2 space-y-1">
                <div v-for="item in navigation" :key="item.name" @click="item.current ? unll : linkTo(item.url)" :class="[item.current ? 'cursor-default' : 'cursor-pointer']">
                        <a  :class="[item.current ? 'bg-gray-100 text-gray-900' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900', 'group flex items-center px-2 py-2 text-base font-medium rounded-md']">
                            <component :is="item.icon" :class="[item.current ? 'text-gray-500' : 'text-gray-400 group-hover:text-gray-500', 'mr-4 flex-shrink-0 h-6 w-6']" aria-hidden="true" />
                            {{ item.name }}
                        </a>
                </div>
              </nav>
            </div>
            <div class="flex-shrink-0 flex border-t border-gray-200 p-4">
              <a href="#" class="flex-shrink-0 group block">
                <div class="flex items-center">
                  <div>
                        <div class="avatar placeholder">
                            <div class="bg-neutral-focus text-neutral-content rounded-full w-10 h-10 uppercase">
                                <span>{{username[0]}}</span>
                            </div>
                        </div>
                    </div>
                  <div class="ml-3">
                    <p class="text-base font-medium text-gray-700 group-hover:text-gray-900">
                      {{username}}
                    </p>
                    
                  </div>
                </div>
              </a>
            </div>
          </div>
        </TransitionChild>
        <div class="flex-shrink-0 w-14">
          <!-- Force sidebar to shrink to fit close icon -->
        </div>
      </Dialog>
    </TransitionRoot>

    <!-- Static sidebar for desktop -->
    <div>
    <div class="hidden md:flex md:w-64 md:flex-col md:fixed md:inset-y-0">
      <!-- Sidebar component, swap this element with another sidebar if you like -->
      <div class="flex-1 flex flex-col min-h-0 border-r border-gray-200 bg-white">
        <div class="flex-1 flex flex-col pt-5 pb-4 overflow-y-auto">
          <div class="flex items-center flex-shrink-0 px-4">
            <router-link to="/gamecenter"> <img class="h-8 w-auto" src="/favicon.svg" alt="Workflow" /> </router-link>
            <span class="text-black font-black mx-4 text-xl"> 个人中心 </span>
          </div>
          <nav class="mt-5 flex-1 px-2 bg-white space-y-1">
            <div v-for="item in navigation" :key="item.name" @click="item.current ? unll : linkTo(item.url)" :class="[item.current ? 'cursor-default' : 'cursor-pointer']">
                <a  :class="[item.current ? 'bg-gray-100 text-gray-900' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900', 'group flex items-center px-2 py-2 text-sm font-medium rounded-md']">
                <component :is="item.icon" :class="[item.current ? 'text-gray-500' : 'text-gray-400 group-hover:text-gray-500', 'mr-3 flex-shrink-0 h-6 w-6']" aria-hidden="true" />
                {{ item.name }}
                </a>
            </div>
          </nav>
        </div>
        <div class="flex-shrink-0 flex border-t border-gray-200 p-4">
          <a href="#" class="flex-shrink-0 w-full group block">
            <div class="flex items-center">
              <div>
                <div class="avatar placeholder">
                    <div class="bg-neutral-focus text-neutral-content rounded-full w-10 h-10 uppercase">
                        <span>{{username[0]}}</span>
                    </div>
                </div>
              </div>
              <div class="ml-3">
                <p class="text-sm font-medium text-gray-700 group-hover:text-gray-900">
                  {{username}}
                </p>
              </div>
            </div>
          </a>
        </div>
      </div>
    </div>
    <div class="md:pl-64 flex flex-col flex-1">
      <div class="sticky top-0 z-10 md:hidden pl-1 pt-1 sm:pl-3 sm:pt-3 bg-gray-100">
        <button type="button" class="-ml-0.5 -mt-0.5 h-12 w-12 inline-flex items-center justify-center rounded-md text-gray-500 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500" @click="sidebarOpen = true">
          <span class="sr-only">Open sidebar</span>
          <MenuIcon class="h-6 w-6" aria-hidden="true" />
        </button>
      </div>
      <component :is="mainComponent"/>
    </div>
  </div>
  </div>
</template>

<script>
import { ref, watch } from 'vue'
import { Dialog, DialogOverlay, TransitionChild, TransitionRoot } from '@headlessui/vue'
import {
  CalendarIcon,
  ChartBarIcon,
  FolderIcon,
  HomeIcon,
  InboxIcon,
  MenuIcon,
  CogIcon,
  AdjustmentsIcon,
  XIcon,
  UserRemoveIcon
} from '@heroicons/vue/outline'

const navigation = [
  { name: 'BOT 管理', component: 'botManagement', url: "manage-bot", icon: AdjustmentsIcon, current: false },
  { name: '个人设置', component: 'Settings', url: "settings", icon: CogIcon, current: false },
]

import axios from 'axios'
import { SERVER_URL } from '@/config'
import BotManagement from './BotManagement.vue'
import Settings from './Settings.vue'
import { useRoute, useRouter } from 'vue-router'

export default {
  components: {
    Dialog,
    DialogOverlay,
    TransitionChild,
    TransitionRoot,
    BotManagement,
    Settings,
    MenuIcon,
    XIcon
  },
  setup() {
    
    const sidebarOpen = ref(false)
    const username = ref('')
    
    axios.get(SERVER_URL + '/api/v1/auth/user')
    .then(res => {
      const data = res.data
      username.value = data.data.username
    })

    let mainComponent;
    const route = useRoute();
    const router = useRouter();
    const mainName = route.params.item;
    
    switch(mainName) {
        case '':
        case 'manage-bot': mainComponent = BotManagement;  navigation[0].current = true; break;
        case 'settings': mainComponent = Settings; navigation[1].current = true; break;
    }

    function linkTo(url) {
        // router.push({path: '/profile/' + url, force: true})
        window.location.href = '/profile/' + url
        // router
    }

    return {
      navigation,
      sidebarOpen,
      username,
      mainComponent,
      linkTo
    }
  },
}
</script>
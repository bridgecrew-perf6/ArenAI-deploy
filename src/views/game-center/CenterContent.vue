<!--
  This example requires Tailwind CSS v2.0+ 
  
  This example requires some changes to your config:
  
  ```
  // tailwind.config.js
  module.exports = {
    // ...
    plugins: [
      // ...
      require('@tailwindcss/aspect-ratio'),
    ],
  }
  ```
-->
<template>
  <div class="bg-white">
    <div class="mx-auto py-12 px-4 max-w-7xl sm:px-6 lg:px-8 lg:py-24">
      <div class="space-y-12">
        <!-- <div class="space-y-5 sm:space-y-4 md:max-w-xl lg:max-w-3xl xl:max-w-none">
          <h2 class="text-3xl font-extrabold tracking-tight sm:text-4xl">全部游戏</h2>
        </div> -->
        <ul role="list" class="space-y-12 sm:grid sm:grid-cols-2 sm:gap-x-6 sm:gap-y-12 sm:space-y-0 lg:grid-cols-3 lg:gap-x-12">
          <li v-for="game in games" :key="game.name">
            <div class="space-y-2">
              <div class="aspect-w-3 aspect-h-2">
                <!-- <router-link :to="'/games/' + game.link"> -->
                <a :href="'/games/' + game.link">
                  <img class="object-cover shadow-lg rounded-lg" :src="game.imageUrl" alt="" />
                </a>
                <!-- </router-link> -->
              </div>

              <div class="space-y-2">
                <div class="text-md leading-6 font-medium">
                  <h3>{{ game.name }}</h3>
                  <p class="text-indigo-600 text-xs">{{ game.type }}</p>
                </div>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
const games = [
  {
    name: '五子棋',
    type: '双人游戏',
    imageUrl: '/gomoku.jpg',
    link: 'gomoku'
  },
  // {
  //   name: '池塘',
  //   type: '4人游戏',
  //   imageUrl: '/gomoku.jpg',
  //   link: 'pond'
  // },
  
]

export default {
  setup() {
    return {
      games,
    }
  },
}
</script>
import {createRouter, createWebHashHistory, createWebHistory} from 'vue-router'
import HomeView from '../views/HomeView.vue'
import MainRoom from "@/views/MainRoom";
import TypingRoom from "@/views/TypingRoom";
import WaitingRoom from "@/views/WaitingRoom";
import WaitingTypingRoom from "@/views/WaitingTypingRoom";
import ResultRoom from "@/views/ResultRoom";
import ResultListRoom from "@/views/ResultListRoom";
import GameOverRoom from "@/views/GameOverRoom";

import store from '../store'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: store.state.roomStartURL + '/main',
    name: 'MainRoom',
    component: MainRoom
  },
  {
    path: store.state.roomStartURL + '/waiting/:room_code',
    name: 'WaitingRoom',
    component: WaitingRoom
  },
  {
    path: store.state.roomStartURL + '/typing/:room_code',
    name: 'TypingRoom',
    component: TypingRoom
  },
  {
    path: store.state.roomStartURL + 'waiting/typing/:room_code',
    name: 'WaitingTypingRoom',
    component: WaitingTypingRoom
  },
  {
    path: store.state.roomStartURL + 'result/:room_code',
    name: 'ResultRoom',
    component: ResultRoom
  },
  {
    path: store.state.roomStartURL + '/result/list/:room_code',
    name: 'ResultListRoom',
    component: ResultListRoom
  },
  {
    path: store.state.roomStartURL + '/gameover/:room_code',
    name: 'GameOverRoom',
    component: GameOverRoom
  },

  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }
]

const router = createRouter({
  //https://router.vuejs.org/guide/essentials/history-mode.html
  //https://stackoverflow.com/questions/34623833/vue-js-how-to-remove-hashbang-from-url
  history: createWebHistory(),
  routes
})

export default router

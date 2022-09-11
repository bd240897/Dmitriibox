import {createRouter, createWebHashHistory, createWebHistory} from 'vue-router'
import HomeView from '../views/HomeView.vue'
import MainRoom from "@/views/MainRoom";

import store from '../store'
import GameRooms from "@/views/GameRooms";
import Login from "@/views/Login";

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
    path: store.state.roomStartURL + '/room/:roomCode',
    name: 'GameRooms',
    component: GameRooms
  },
  {
    path: '/vue' + '/login',
    name: 'Login',
    component: Login
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

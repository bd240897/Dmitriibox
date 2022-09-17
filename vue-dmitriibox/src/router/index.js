import {createRouter, createWebHashHistory, createWebHistory} from 'vue-router'
import HomeView from '../views/HomeView.vue'
import MainRoom from "@/views/MainRoom";

import store from '../store'
import GameRooms from "@/views/GameRooms";
import Login from "@/views/Login";
import test_resize from "@/views/test_resize";
import test_mixins from "@/views/test_mixins";

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/vue/room' + '/main',
    name: 'MainRoom',
    component: MainRoom
  },
  {
    path: '/vue/room' + '/game',
    name: 'GameRoom',
    component: GameRooms
  },
  {
    path: '/vue/room' + '/login',
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
  },
  /////////////////////// TEST /////////////////////////////
  {
    path: '/test_resize',
    name: 'test_resize',
    component: test_resize
  },
  {
    path: '/test_mixins',
    name: 'test_mixins',
    component: test_mixins
  },
]

const router = createRouter({
  //https://router.vuejs.org/guide/essentials/history-mode.html
  //https://stackoverflow.com/questions/34623833/vue-js-how-to-remove-hashbang-from-url
  history: createWebHistory(),
  routes
})

export default router

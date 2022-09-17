import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from "./store";
import Vue from 'vue'

const app = createApp(App).use(router).use(store)
app.mount('#app')

export default app



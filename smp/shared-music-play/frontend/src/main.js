import { createApp } from 'vue'
import App from './App.vue'
import { createPinia } from 'pinia';
import router from "./router";
import { createManager } from '@vue-youtube/core';

const pinia = createPinia();
const manager = createManager();

let app = createApp(App)
app.use(router)
app.use(pinia)
app.use(manager)
app.mount('#app')

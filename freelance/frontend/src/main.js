import Vue, {createApp} from '@vue/compat'
import {BootstrapVue} from 'bootstrap-vue'
import App from './App.vue'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import './assets/main.css'
import router from './router'
import {createPinia} from 'pinia'

Vue.use(BootstrapVue)
const app = createApp(App)
app.use(createPinia())
app.use(router)

app.mount('#app')

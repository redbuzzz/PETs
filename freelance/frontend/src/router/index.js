import { createRouter, createWebHistory } from 'vue-router'
import Home from "@/views/Home.vue";
import LoginPage from "@/views/LoginPage.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomeVue',
      component: Home
    },
    {
      path: '/login',
      name: 'LoginVue',
      component: LoginPage
    },

  ]
})

export default router

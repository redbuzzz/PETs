import {createRouter, createWebHistory} from 'vue-router'
import {useAuthStore} from "@/stores/authStore";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: () => import('../views/HomeView.vue'),
            meta: {unauthorizedAccess: true}

        },
        {
            path: '/login',
            name: 'login',
            component: () => import('../views/AuthVue.vue'),
            meta: {unauthorizedAccess: true}
        },
        {
            path: '/profile',
            name: 'profile',
            component: () => import('../views/ProfileVue.vue'),
            meta: {unauthorizedAccess: true}
        },
    ]
});

router.beforeEach((to, from) => {
    const isUnauthorizedAccessAllowed = to.meta?.unauthorizedAccess === true;
    const authStore = useAuthStore();
    if (!authStore.isAuth && !isUnauthorizedAccessAllowed && from.name !== 'login') {
        return {name: "login"};
    }
});


export default router;


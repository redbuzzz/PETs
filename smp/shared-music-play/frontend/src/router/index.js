import {createRouter, createWebHistory} from 'vue-router'
import Login from '@/views/Login.vue'
import Search from "@/views/Search.vue";
import Home from "@/views/Home.vue";
import Room from "@/views/Room.vue";
import MainPage from "@/views/MainPage.vue";
import Registration from "../views/Registration.vue";
import Profile from "@/views/Profile.vue";

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/login',
        name: 'Login',
        component: Login
    },
    {
        path: '/register',
        name: 'Registration',
        component: Registration
    },
    {
        path: '/search',
        name: 'Search',
        component: Search
    },
    {
        path: '/room',
        redirect: {name: 'Main'},
        children: [
            {
                path: ':id',
                name: 'Room',
                component: Room
            }
        ],
    },
    {
        path: '/main',
        name: 'Main',
        component: MainPage
    },
    {
        path: '/profile',
        name: 'Profile',
        component: Profile
    },
    {
        path: '/:pathMatch(.*)*',
        redirect: {name: 'Home'}
    }
]
const router = createRouter({
    history: createWebHistory(),
    routes
})
export default router

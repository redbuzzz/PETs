import {createRouter, createWebHistory} from 'vue-router'
import {useWebSocketStore} from "@/stores/WebsocketStore";
import {useRoomStore} from "@/stores/RoomStore";
import {nextTick} from "vue";
import {useUserStore} from "@/stores/UserStore";

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: {unauthorizedAccess: true}
  },
  {
    path: '/register',
    name: 'Registration',
    component: () => import('@/views/Registration.vue'),
    meta: {unauthorizedAccess: true}
  },
  {
    path: '/room',
    redirect: {name: 'Main'},
    children: [
      {
        path: ':id',
        name: 'Room',
        component: () => import('@/views/Room.vue')
      }
    ],
  },
  {
    path: '/main',
    name: 'Main',
    component: () => import('@/views/MainPage.vue')
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/Profile.vue')
  },
  {
    path: '/logout',
    name: "Logout",
    component: () => import('@/views/Logout.vue'),
  }
]
const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from) => {
  if (from.name === 'Room') {
    useWebSocketStore().closeConnection();
    await nextTick();
    useRoomStore().clearActiveRoom();
  }
  const userStore = useUserStore();
  const isUnauthorizedAccessAllowed = to.meta?.unauthorizedAccess || false;
  if (!userStore.isAuth && !isUnauthorizedAccessAllowed && (from.name !== "Login" || from.name !== "Registration")) {
    console.log('unauthorized')
    return {name: "Login"};
  } else if (userStore.isAuth && (to.name === "Login" || to.name === "Registration")) {
    return {name: "Main"}
  } else if (userStore.isAuth && userStore.profileInfo.id === null) {
    await userStore.profileData();
  }
})
export default router

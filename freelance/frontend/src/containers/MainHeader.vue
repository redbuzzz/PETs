<template>
    <b-navbar toggleable="lg" :type="isDark ? 'dark' : 'light'" :variant="isDark ? 'dark' : 'light'" class="navbar">
        <b-container>
            <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
            <b-collapse id="nav-collapse" is-nav>
                <b-navbar-nav>
                    <b-nav-item :to="{name: 'home'}" class="h3">Главная</b-nav-item>
                    <b-nav-item v-if="!isAuth" :to="{name: 'login'}" class="h3">Вход</b-nav-item>
                    <b-nav-item v-else @click="logoutHandler" class="h3">Выйти</b-nav-item>
                </b-navbar-nav>
            </b-collapse>
            <b-navbar-nav class="ml-auto">
                <b-nav-item v-if="isAuth" :to="{name: 'profile'}" class="h3">{{ user.email }}</b-nav-item>
                <b-avatar v-if="isDark" button @click="toggleTheme" variant="warning" src="public/moon.png" size="3rem"
                          class=" dark-theme image-top"></b-avatar>
                <b-avatar v-else button @click="toggleTheme" variant="warning" src="public/sun.png" size="3rem"
                          class="light-theme image-top"></b-avatar>
            </b-navbar-nav>
        </b-container>
    </b-navbar>
</template>

<script>
import {mapActions, mapState} from "pinia";
import {useAuthStore} from "@/stores/authStore";
import {nextTick} from "vue";

export default {
    name: "MainHeader",
    computed: {
        ...mapState(useAuthStore, ['user', 'isAuth', 'isDark']),
    },
    methods: {
        ...mapActions(useAuthStore, ['logout', 'toggle']),
        async logoutHandler() {
            await this.logout()
            await nextTick()
            this.$router.push({name: 'login'});
        },
        async toggleTheme() {
            await this.toggle()
        },
    }
}
</script>

<style scoped>
.navbar-text {
    color: #d5d5d5;
}

.navbar {
    height: 70px;

}
.image-top {
    margin: auto 0;
}
</style>
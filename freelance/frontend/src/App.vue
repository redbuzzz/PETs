<script setup>
import {RouterView} from 'vue-router'
import MainHeader from "@/containers/MainHeader.vue";
</script>

<template>
    <div :style="isDark ? 'background-color: #2e353c' : 'background-color: #ffffff'" class="MainDiv">
    <MainHeader class="mb-3"/>
    <RouterView/>
    </div>
</template>

<style>
.MainDiv {
    min-height: 100vh;
}
</style>

<script>
import {mapActions, mapState} from "pinia";
import {useAuthStore} from "@/stores/authStore";

export default {
    name: "App",
    created() {
        this.load();
    },
    methods: mapActions(useAuthStore, ['load']),
    computed: mapState(useAuthStore, ['isDark'])
}
</script>

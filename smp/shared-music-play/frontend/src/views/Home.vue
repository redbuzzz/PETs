<template>
  <BaseComponent>
    <MainContainer>
      <div id="nav" style="display: flex; justify-content: space-between; width: 100%">
        <router-link to="/login">Login</router-link>
        <hr>
        <router-link to="/search">Search</router-link>
        <hr>
        <router-link to="/room">Room</router-link>
        <hr>
        <router-link to="/main">Main</router-link>
        <hr>
        <router-link to="/register">Register</router-link>
      </div>
    </MainContainer>
  </BaseComponent>
</template>

<script>
import BaseComponent from "@/components/containers/BaseContainer.vue";
import MainContainer from "@/components/containers/MainContainer.vue";

export default {
  name: "Home",
  components: {MainContainer, BaseComponent}
}
</script>

<style scoped>
* {
  color: #D9D9D9;
}
</style>

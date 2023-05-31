<template>
  <BaseComponent>
    <MainContainer>
      <LoginForm/>
    </MainContainer>
  </BaseComponent>
</template>

<script>

import BaseComponent from "@/components/containers/BaseContainer.vue";
import MainContainer from "@/components/containers/MainContainer.vue";
import LoginForm from "@/components/elements/auth/LoginForm.vue";
import {useUserStore} from "@/stores/UserStore";

export default {
  name: "Login",
  components: {LoginForm, MainContainer, BaseComponent},
  mounted() {
    useUserStore().clearError();
  }
}
</script>

<style scoped>

</style>

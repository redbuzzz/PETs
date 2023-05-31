<template>
  <BaseComponent>
    <MainContainer>
      <RegistrationForm/>
    </MainContainer>
  </BaseComponent>
</template>

<script>

import BaseComponent from "@/components/containers/BaseContainer.vue";
import MainContainer from "@/components/containers/MainContainer.vue";
import RegistrationForm from "../components/elements/auth/RegistrationForm.vue";
import {useUserStore} from "@/stores/UserStore";

export default {
  name: "Registration",
  components: {RegistrationForm, MainContainer, BaseComponent},
  mounted() {
    useUserStore().clearError();
  }
}
</script>

<style scoped>

</style>

<template>
  <Spinner :flag="loading"/>
  <BaseAuthForm
      @submit.prevent="this.submit"
      :title="this.title"
      :action-name="this.actionName"
      :links="this.links"
      :error="this.error">

    <InputBlock name="email" required="required" v-model="this.form.email"/>
    <InputBlock name="password" required="required" v-model="this.form.password"/>

  </BaseAuthForm>
</template>

<script>
import BaseAuthForm from "./BaseAuthForm.vue";
import InputBlock from "./InputBlock.vue";
import {API_URL} from "@/services/consts";
import {useUserStore} from "@/stores/UserStore";
import {mapActions, mapState} from "pinia";
import Spinner from "@/components/elements/Spinner.vue";

export default {
  name: "RegistrationForm",
  methods: {
    API_URL,
    ...mapActions(useUserStore, ['register']),
    async submit() {
      await this.register(this.form.email, this.form.password);
      if (!this.error) {
        this.$router.push({name: 'Main'});
      }
    }
  },
  components: {Spinner, InputBlock, BaseAuthForm},
  data() {
    return {
      title: "Register",
      actionName: "Sign up",
      form: {
        email: '',
        password: ''
      },
      links: [
        {
          link: "/login",
          name: "Sign in"
        }
      ]
    }
  },
  computed: {
    ...mapState(useUserStore, {
      error: (state) => state.requestData.error,
      loading: state => state.requestData.loading
    })
  }
}
</script>

<style scoped>

</style>

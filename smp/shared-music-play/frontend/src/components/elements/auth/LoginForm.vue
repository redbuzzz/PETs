<template>
  <Spinner :flag="this.loading"/>
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
import {mapActions, mapState} from "pinia";
import {useUserStore} from "@/stores/UserStore";
import Spinner from "@/components/elements/Spinner.vue";

export default {
  name: "LoginForm",
  methods: {
    API_URL,
    ...mapActions(useUserStore, ['login']),
    async submit() {
      await this.login(this.form.email, this.form.password);
      if (!this.error) {
        this.$router.push({name: 'Main'});
      }
    }
  },
  components: {Spinner, InputBlock, BaseAuthForm},
  data() {
    return {
      title: "Login",
      form: {
        email: '',
        password: ''
      },
      actionName: "Sign in",
      links: [
        {
          link: "/register",
          name: "Sign up"
        }
      ]
    }
  },
  computed: {
    ...mapState(useUserStore, {
      error: state => state.requestData.error,
      loading: state => state.requestData.loading
    })
  }
}
</script>

<style scoped>

</style>

<template>
  <Spinner :flag="this.loading"/>
  <BaseAuthForm
      @submit.prevent="this.submit"
      :title="this.title"
      :action-name="this.actionName"
      :links="this.links"
      :error="this.error">

      <InputBlock name="email" required="required" v-model="this.form.email" :errors="this.fieldErrors.email" />
      <InputBlock name="password" required="required" v-model="this.form.password" :errors="this.fieldErrors.password" />

  </BaseAuthForm>
</template>

<script>
import BaseAuthForm from "./BaseAuthForm.vue";
import InputBlock from "./InputBlock.vue";
import {API_URL} from "@/services/consts";
import {mapActions, mapState} from "pinia";
import {useUserStore} from "@/stores/UserStore";
import Spinner from "@/components/elements/Spinner.vue";
import useVuelidate from "@vuelidate/core";
import {email, helpers, maxLength, minLength, required} from "@vuelidate/validators";
import _ from "lodash";
import FormValidationMixin from "../../../mixins/FormValidationMixin";

export default {
  // setup() {
  //   return {
  //     v$: useVuelidate()
  //   }
  // },
  name: "LoginForm",
  mixins: [FormValidationMixin],
  methods: {
    API_URL,
    ...mapActions(useUserStore, ['login']),
    async submit() {
      this.v$.form.$touch();
      if (this.v$.form.$error) {
        return;
      }
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
  validations: {
    form: {
      email: {
        required: helpers.withMessage("This field is required", required),
        email: helpers.withMessage("Not a valid email", email),
      },
      password: {
        required: helpers.withMessage("This field is required", required),
        minLength: helpers.withMessage("Min length is 5 characters", minLength(5)),
        maxLength: helpers.withMessage("Max length is 255 characters", maxLength(255))
      }
    }
  },
  computed: {
    ...mapState(useUserStore, {
      error: state => state.requestData.error,
      loading: state => state.requestData.loading
    }),
  }
}
</script>

<style scoped>

</style>

<template>
  <Spinner :flag="loading"/>
  <BaseAuthForm
      @submit.prevent="this.submit"
      :title="this.title"
      :action-name="this.actionName"
      :links="this.links"
      :error="this.error">

        <InputBlock name="name" v-model="this.form.name" :errors="this.fieldErrors.name"/>
        <InputBlock name="email" v-model="this.form.email" :errors="this.fieldErrors.email"/>
        <InputBlock name="password" v-model="this.form.password" :errors="this.fieldErrors.password"/>

  </BaseAuthForm>
</template>

<script>
import BaseAuthForm from "./BaseAuthForm.vue";
import InputBlock from "./InputBlock.vue";
import {API_URL} from "@/services/consts";
import {useUserStore} from "@/stores/UserStore";
import {mapActions, mapState} from "pinia";
import Spinner from "@/components/elements/Spinner.vue";
import {email, helpers, maxLength, minLength, required} from "@vuelidate/validators";
import useVuelidate from "@vuelidate/core";
import _ from "lodash";
import FormValidationMixin from "../../../mixins/FormValidationMixin";

export default {
  name: "RegistrationForm",
  mixins: [FormValidationMixin],
  methods: {
    API_URL,
    ...mapActions(useUserStore, ['register']),
    async submit() {
      this.v$.form.$touch();
      if (this.v$.form.$error) {
        return;
      }
      await this.register(this.form.name, this.form.email, this.form.password);
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
      v$: useVuelidate(),
      form: {
        name: '',
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
  validations: {
    form: {
      email: {
        required: helpers.withMessage("This field is required", required),
        email: helpers.withMessage("Not a valid email", email),
      },
      name: {
        required: helpers.withMessage("This field is required", required),
        minLength: helpers.withMessage("Min length is 5 characters", minLength(5)),
        maxLength: helpers.withMessage("Max length is 255 characters", maxLength(255))
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
      error: (state) => state.requestData.error,
      loading: state => state.requestData.loading
    }),
  }
}
</script>

<style scoped>

</style>

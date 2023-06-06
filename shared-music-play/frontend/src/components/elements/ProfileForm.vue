<template>
  <div class="profile">

    <form class="form" @submit.prevent="updateProfile">
      <div v-if="this.requestData.error" class="error">{{ this.requestData.error.message }}</div>
      <input-block label="Your name"
                   class="search-bar"
                   v-model="form.name"
                   placeholder="Enter your name"
                   :errors="this.fieldErrors.name"/>
      <div class="success-message" v-if="successMessage!==null">{{ successMessage }}</div>
      <div class="loading" v-if="this.requestData.loading">
        <span class="spinner-overlay"></span>
        <span class="spinner"></span>
      </div>
      <input-block label="Your email"
                   v-model="form.email"
                   placeholder="Enter your email"
                   :errors="this.fieldErrors.email"/>
      <button type="submit">Update profile information</button>
    </form>
  </div>
</template>

<script>

import InputBlock from "@/components/elements/auth/InputBlock.vue";

import {mapActions, mapState} from "pinia";
import {useUserStore} from "@/stores/UserStore";
import useVuelidate from "@vuelidate/core";
import {email, helpers, maxLength, minLength, required} from "@vuelidate/validators";
import _ from "lodash";
import FormValidationMixin from "../../mixins/FormValidationMixin";

export default {
  name: "ProfileForm",
  components: {InputBlock},
  mixins: [FormValidationMixin],
  setup() {
    return {
      v$: useVuelidate()
    }
  },
  data() {
    return {
      form: {
        name: '',
        email: '',
      },
      isUpdated: false
    };
  },
  async created() {
    await this.profileData();
    this.form.name = this.profileInfo?.name;
    this.form.email = this.profileInfo?.email;
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
    }
  },
  computed: {
    ...mapState(useUserStore, ['profileInfo', 'requestData']),
    error() {
      return this.requestData.error;
    },
    successMessage() {
      if (this.isUpdated) {
        return "Successfully updated!"
      }
      return null
    }
  },
  methods: {
    ...mapActions(useUserStore, ['profileData', 'updateProfileData']),
    async updateProfile() {
      this.v$.form.$touch();
      if (this.v$.form.$error) {
        return;
      }
      this.isUpdated = await this.updateProfileData(this.form.email, this.form.name)
      setTimeout(() => {this.isUpdated = false}, 2500)
    }
  },
};
</script>

<style scoped>
.error {
  color: red;
  text-align: center;
}

.profile {
  display: flex;
  flex-direction: column;
  margin: auto;
  gap: 20px;
}

div {
  color: white;
}

.spinner {
  position: fixed;
  margin: 0 auto;
  width: 50px;
  height: 50px;
  border: 5px solid rgba(0, 0, 0, 0.1);
  border-left-color: #09f;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.form {
  display: flex;
  justify-content: center;
  flex-direction: column;
}

.loading {
  display: flex;
  justify-content: center;
}

.success-message {
  background-color: #282c34;
  color: #ffffff;
  border: 2px solid #00ff00;
  padding: 10px;
  border-radius: 5px;
}

.spinner-overlay {
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  background-color: rgba(0, 0, 0, 0.5);
}
</style>

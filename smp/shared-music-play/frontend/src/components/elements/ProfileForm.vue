<template>
  <div class="profile">

    <form class="form" @submit.prevent="updateProfile">
      <div v-if="this.requestData.error">{{ this.requestData.error.message }}</div>
      <input-block label="Your name" class="search-bar" v-model="form.name" placeholder="Enter your name"/>
      <div class="success-message" v-if="successMessage!==null">{{ successMessage }}</div>
      <div class="loading" v-if="this.requestData.loading">
        <span class="spinner-overlay"></span>
        <span class="spinner"></span>
      </div>
      <input-block label="Your email" v-model="form.email" placeholder="Enter your email"/>
      <button type="submit">Update profile information</button>
    </form>
  </div>
</template>

<style scoped>
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

<script>

import InputBlock from "@/components/elements/auth/InputBlock.vue";

import {mapActions, mapState} from "pinia";
import {nextTick} from "vue";
import {useUserStore} from "@/stores/UserStore";

export default {
  name: "ProfileForm",
  components: {InputBlock},
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
  computed: {
    ...mapState(useUserStore, ['profileInfo', 'requestData']),
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
      this.isUpdated = await this.updateProfileData(this.form.email, this.form.name)
      setTimeout(() => {this.isUpdated = false}, 2500)
    }
  },
};
</script>

<template>
  <div class="profile">
    <input-block label="Your name" class="search-bar" v-model="inputName" placeholder="Enter your name"/>
    <input-block  label="Your email" v-model="inputEmail" placeholder="Enter your email"/>
    <button @click="updateProfile">Update Profile</button>
      <div>
      Your email: {{ updatedEmail || email }}
      <br>
      Your name: {{ updatedName || name }}
      <p v-if="success">Successfully updated!</p>
      </div>
  </div>
</template>

<style scoped>
.profile{
  display: flex;
  flex-direction: column;
  margin: auto;
  gap: 20px;
}

div {
  color: white;
}
</style>

<script>

import InputBlock from "@/components/elements/auth/InputBlock.vue";
import axios from "axios";
import {API_URL} from "@/services/consts";

export default {
  name: "ProfileForm",
  components: {InputBlock},
  data() {
    return {

      name: "",
      email: "",
      inputName: "",
      inputEmail: "",
      updatedName: "",
      updatedEmail: "",
      loading: false,
      success: null,
    };
  },
  created() {
    this.fetchProfileData();
  },
  methods: {
    fetchProfileData() {
      this.loading = true;
      axios
          .get(`${API_URL}/profile`, {
            headers: {
              Authorization: `Token ${localStorage.getItem("token")}`,
            },
          })
          .then((response) => {
            this.name = response.data.name;
            this.email = response.data.email;
            this.inputName = response.data.name;
            this.inputEmail = response.data.email;
          })
          .catch((error) => {
            console.error("Ошибка при отправке запроса:", error);
          })
          .finally(() => {
            this.loading = false;
          });
    },
    updateProfile() {
      this.success = null
      this.loading = true;
      this.updatedName = this.inputName;
      this.updatedEmail = this.inputEmail;
      this.name = this.inputName;
      this.email = this.inputEmail;
      axios.put(
          `${API_URL}/profile`,
          {name: this.inputName, email: this.inputEmail},
          {
            headers: {
              Authorization: `Token ${localStorage.getItem("token")}`,
            },
          }
      )
          .then((response) => {
            console.log("Профиль успешно обновлен:", response.data);
          })
          .catch((error) => {
            console.error("Ошибка обновления профиля:", error);
          })
          .finally(() => {
            this.loading = false;
            this.success = true
          });
    },
  },
};
</script>

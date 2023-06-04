<template>
  <form class="form" @submit="this.$emit('submit.prevent')">
    <div class="form-title">
      {{ title }}
    </div>
    <div class="form-error" v-if="this.error">
        {{ error.message }}
    </div>

    <slot>

    </slot>

    <div class="input-block">
      <button class="sign-button">
        {{ this.actionName }}
      </button>
    </div>

    <router-link v-for="link in links"
                 :to="link.link"
                 >
        {{ link.name }}
    </router-link>
  </form>
</template>

<script>
import InputBlock from "./InputBlock.vue";

export default {
  name: 'BaseAuthForm',
  components: {InputBlock},
  props: {
    title: String,
    actionName: String,
    links: Array,
    error: Error
  }
}
</script>

<style scoped>

* {
  color: #FFF;
  text-decoration: none;
}

.input-colors{
  color: #1F1F1F
}

.form {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #1F1F1F;
  margin: 30px auto 70px auto;
  padding: 30px;
  width: 420px;
  min-height: 600px;
  max-height: 600px;
}

.form-title {
  font-size: 42px;
  margin: 30px 0;
  text-align: center;
}

.form-error {
    color: red;
    margin: 0;
    text-align: center;
    font-size: 30px;
}

.input-block {
  margin: 30px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-shrink: 1;
  max-width: 80%;
}

.sign-button {
  padding: 10px 15px;
  background: #999999;
}


</style>

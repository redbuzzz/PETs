<script>
import {defineComponent} from 'vue'

export default defineComponent({
    name: "Spinner",
    props: {
        flag: Boolean,
    }
})
</script>

<template>
    <div v-if="flag" class="spinner-overlay">
        <div class="spinner"></div>
    </div>
</template>

<style scoped lang="scss">
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
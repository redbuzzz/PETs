<template>
  <div class="whole-page">
    <NavBar/>
    <slot>
    </slot>
  </div>
</template>

<script>
import NavBar from "@/components/elements/NavBar.vue";

export default {
  name: "BaseContainer",
  components: {NavBar}
}
</script>

<style scoped>
.whole-page {
  display: flex;
  flex-direction: row;
  width: 100%;
  height: 100%;
  max-height: 100%;
  background-color: #3C3C3C;
}
</style>

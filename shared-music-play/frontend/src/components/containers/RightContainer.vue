<template>
  <div class="right-block">
    <slot/>
  </div>
</template>

<script>
export default {
  name: "RightContainer"
}
</script>

<style scoped>
.right-block {
  height: 100%;
  overflow: hidden;
  margin-left: 10px;
  width: 100%;
  max-width: 500px;
  min-width: 300px;
  display: flex;
  flex-direction: column;
}
</style>

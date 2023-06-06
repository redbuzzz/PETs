<template>
  <div class="left-block">
    <slot/>
  </div>
</template>

<script>

export default {
  name: "LeftContainer",
}
</script>

<style scoped>
.left-block {
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  overflow: hidden;
}
</style>

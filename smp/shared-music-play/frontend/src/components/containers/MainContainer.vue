<template>
  <div class="main-page-part">
    <div class="main-content-block">
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: "MainContainer"
}
</script>

<style scoped>
.main-page-part {
  padding: 30px;
  width: 100%;
}

.main-content-block {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: row;
}
</style>

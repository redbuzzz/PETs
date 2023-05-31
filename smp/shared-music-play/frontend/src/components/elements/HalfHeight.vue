<template>
  <div>
    <slot>
    </slot>
  </div>
</template>

<script>
export default {
  name: "HalfHeight"
}
</script>

<style scoped>
div {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 50px;
  background-color: #1F1F1F;
}
</style>
<template>
  <div class="search-results scroll-block">
    <slot/>
  </div>
</template>

<script>

export default {
  name: "ItemsList"
}
</script>

<style scoped>
.search-results {
  display: flex;
  flex-direction: column;
  max-height: calc(100% - 60px);
}
</style>

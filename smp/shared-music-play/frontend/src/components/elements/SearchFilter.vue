<template>
  <input @input="$emit('update:modelValue', $event.target.value)"
         class="search-bar full-width small"
         :value="modelValue"
         :placeholder="placeholder">
</template>

<script>
export default {
  name: "SearchFilter",
  props: {
    placeholder: {
      type: String,
      default: "Search"
    },
    modelValue: {
      type: String,
      required: true
    }
  },
  emits: ["update:modelValue"],
}
</script>

<style scoped>
.search-bar {
  height: 45px;
  width: 100%;
  margin-bottom: 10px;
}

.search-bar form {
  display: flex;
  flex-direction: row;
}
</style>

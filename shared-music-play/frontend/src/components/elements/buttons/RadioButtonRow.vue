<template>
  <div class="radio-row">
    <label v-for="option in options"
           class="radio-label"
           :class="{active: modelValueComputed === option.value}">
      <input type="radio"
             class="radio"
             :name="option.name"
             :value="option.value"
             v-model="modelValueComputed"
      >
      {{ option.label }}
    </label>
  </div>
</template>

<script>
export default {
  name: "RadioButtonRow",
  props: ['options', 'modelValue'],
  computed: {
    modelValueComputed: {
      get() {
        return this.modelValue
      },
      set(value) {
        this.$emit('update:modelValue', value)
      }
    }
  },
  methods: {
    change() {
      this.modelValue = this.value;
      this.$emit('update:modelValue', this.modelValue)
    }
  }
}
</script>

<style scoped>

.radio-label {
    width: 200px;
    height: 40px;
    margin-right: 30px;
    background: #D9D9D9;
    display: flex;
    align-items: center;
    justify-content: center;
}

.radio-label:last-child {
    margin-right: 0;
}

.radio-row {
    display: flex;
    margin: 20px 0;
}

.radio {
    display: none;
}

.radio-label.active {
    opacity: .8;
}

</style>

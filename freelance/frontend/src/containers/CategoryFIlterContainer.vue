<template>

    <b-form-select
            :options="options" :value="modelValue" @change="setValue" class="custom-select"/>
</template>


<script>
import {getCategory} from "@/services/api";

export default {
    name: "CategoryFilterContainer",
    emits: ['update:modelValue'],
    props: {
        modelValue: String
    },
    data() {
        return {
            results: []
        }
    },
    methods: {
        async load() {
            this.results = await getCategory()
        },
        setValue(value) {
            this.$emit("update:modelValue", value);
        }
    },
    created() {
        this.load()
    },
    computed: {
        options() {
            return [
                {value: null, text: "Выберите категорию"},
                ...this.results.map(x => ({value: x.id, text: x.name}))
            ]
        }
    }
}
</script>
<style scoped>
.custom-select:hover {
    cursor: pointer;
}
.custom-select {
  /* Добавьте свои стили для красивой стилизации выпадающего списка */
  /* Ниже приведен пример стилей */
  width: 200px;
  height: 40px;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 8px;
  font-size: 14px;
  color: #333;
}

.custom-select:focus {
  outline: none;
  border-color: #aaa;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
}

.custom-select option {

  background-color: #fff;
  color: #333;
}

.custom-select option:checked {

  background-color: #007bff;
  color: #fff;
}

.custom-select option:hover {

  background-color: #f5f5f5;
}

.custom-select option:before {

  content: "\2022";
  margin-right: 5px;
}
</style>
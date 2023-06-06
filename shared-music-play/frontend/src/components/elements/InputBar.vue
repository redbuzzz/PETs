<template>
    <div class="search-bar">
        <form @submit.prevent="this.$emit('search', this.modelValue)">
            <input class="full-width small"
                   :placeholder="placeholder"
                   :value="modelValue"
                   @input="$emit('update:modelValue', $event.target.value)"
            />
            <button style="width: 140px" class="small white-bg" type="submit">{{ button_text }}</button>
        </form>
    </div>
</template>

<script>
export default {
    name: "InputBar",
    props: {
        placeholder: String,
        button_text: String,
        modelValue: String
    },
};
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


.input-string:hover, .input-string:focus {
    outline: None;
}
</style>

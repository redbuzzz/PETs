<template>
    <div class="search-bar">
        <form @submit.prevent="submitForm">
            <input class="full-width small" :placeholder="placeholder" v-model="searchText" />
            <button style="width: 140px" class="small white-bg" type="submit">{{ button_text }}</button>
        </form>
    </div>
</template>

<script>
export default {
    name: "InputBar",
    props: {
        placeholder: String,
        button_text: String
    },
    data() {
        return {
            searchText: ""
        };
    },
    created() {
        const query = this.$route.query.q;
        if (query) {
            this.searchText = query;
            this.submitForm();
        }
    },
    methods: {
        submitForm() {
            this.$emit("search", this.searchText);
        }
    }
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

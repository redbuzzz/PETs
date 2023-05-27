<template>
    <b-card border-variant="secondary" :bg-variant="isDark ? 'dark' : 'white'" :text-variant="isDark ? 'white' : 'dark'">
        <form action="" @submit.prevent="submit">
            <b-input placeholder="Поиск..." size="lg" v-model="search"></b-input>
            <category-f-ilter-container :model-value="catId" class="mt-4" size="lg"
                                        @update:model-value="catId=$event"></category-f-ilter-container>
            <b-button block type="submit" :variant="isDark ? 'outline-light' : 'outline-primary'" class="margin-left btn-lg" size="lg">ОК</b-button>
        </form>
    </b-card>
</template>

<script>


import CategoryFIlterContainer from "@/containers/CategoryFIlterContainer.vue";
import {mapActions, mapState} from "pinia";
import {useTaskStore} from "@/stores/taskStore";
import {useAuthStore} from "@/stores/authStore";

export default {
    name: "TaskFilterContainer",
    components: {CategoryFIlterContainer},
    methods: {
        ...mapActions(useTaskStore, ['setParameter', 'load', 'setParameters']),
        submit() {
            this.load()
            this.$router.push({query: this.params})

        },
    },
    created() {
        this.setParameters(this.$route.query)
        this.load()
    },
    computed: {
        ...mapState(useTaskStore, ['params']),
        ...mapState(useAuthStore, ['isDark']),
        search: {
            get() {
                return this.params.search
            },
            set(value) {
                this.setParameter('search', value)
            }
        },
        catId: {
            get() {
                return this.params.category_id || null
            },
            set(value) {
                this.setParameter('category_id', value)
            }
        },
    }

}
</script>

<style scoped>
.margin-left {
    margin-left: 0.5%;
}
</style>
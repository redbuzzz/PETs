<template>
    <SkeletonContainer v-if="isLoading"/>
    <div>
        <!--        todo справа у карточки выводить аватарку создателя чтобы можно было перейти к нему в профиль-->
        <b-card border-variant="secondary" :bg-variant="isDark ? 'dark' : 'white'"
                :text-variant="isDark ? 'white' : 'dark'" v-for="task in results"
                :key="task.id">
            <b-button size="lg" class="position-absolute top-1 end-0"
                      :variant="isDark ? 'outline-light' : 'outline-primary'">Заявка
            </b-button>
            <b-card-title class="h2">{{ task.title }}</b-card-title>
            <b-card-text class="h2-m">{{ task.description }}</b-card-text>
            <b-link href="#" class="card-link">Другая ссылка</b-link>
            <b-card-footer v-for="name in task.tag_names" :key="name.id">Теги:
                <b-badge :variant="isDark ? 'light' : 'dark'" :class="isDark ? 'text-white' : 'text-black'">{{
                    name
                    }}
                </b-badge>
                <br>
                Категория: {{ task.category.name }}
            </b-card-footer>
        </b-card>

    </div>
</template>


<script>
import {mapActions, mapState} from "pinia";
import {useTaskStore} from "@/stores/taskStore";
import {useAuthStore} from "@/stores/authStore";
import SkeletonContainer from "@/containers/SkeletonContainer.vue";

export default {
    name: "TaskContainer",
    components: {SkeletonContainer},
    methods: mapActions(useTaskStore, ['load']),
    computed: {
        ...mapState(useTaskStore, ['isLoading', 'results']),
        ...mapState(useAuthStore, ['isDark']),
    },
    created() {
        this.load()
    }
}
</script>


<style scoped>

</style>
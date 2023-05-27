<template>
    <div>
        <b-container fluid class="custom-container">
            <TaskFilterContainer/>
            <TaskContainer/>
        </b-container>
    </div>


</template>
<script>
import TaskFilterContainer from "@/containers/TaskFilterContainer.vue";
import TaskContainer from "@/containers/TaskContainer.vue";
import {mapState} from "pinia";
import {useAuthStore} from "@/stores/authStore";

export default {
    components: {TaskContainer, TaskFilterContainer},
    computed: mapState(useAuthStore, ['isDark'])
}
</script>

<style>

</style>
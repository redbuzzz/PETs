<template>
    <BaseComponent>
        <MainContainer>
            <ProfileForm/>
        </MainContainer>
    </BaseComponent>
</template>

<script>
import BaseComponent from "@/components/containers/BaseContainer.vue";
import MainContainer from "@/components/containers/MainContainer.vue";
import ProfileForm from "@/components/elements/ProfileForm.vue";

export default {
    name: "ProfileCheck",
    components: {ProfileForm, MainContainer, BaseComponent}
}
</script>



<style scoped >

</style>

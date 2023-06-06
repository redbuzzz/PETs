<template>

</template>

<script>
import {clearTokens} from "@/services/localData";
import {useUserStore} from "@/stores/UserStore";
import router from "@/router";
import {useRoomStore} from "@/stores/RoomStore";

export default {
  name: "Logout",
  created() {
    clearTokens();
    useUserStore().$reset();
    useRoomStore().$reset();
    router.push({name: "Login"});
  }
}
</script>

<style scoped>

</style>
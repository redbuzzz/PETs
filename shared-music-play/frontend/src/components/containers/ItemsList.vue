<template>
  <div class="search-results scroll-block">
    <Spinner :flag="loading"/>
    <slot/>
  </div>
</template>

<script>

import Spinner from "@/components/elements/Spinner.vue";
import {mapState, mapWritableState} from "pinia";
import {useRoomStore} from "@/stores/RoomStore";

export default {
  name: "ItemsList",
  components: {Spinner},
  computed: {
    ...mapWritableState(useRoomStore, {
      loading: state => state.roomsRequestData.loading,
    })
  }
}
</script>

<style scoped>
.search-results {
  display: flex;
  flex-direction: column;
  max-height: calc(100% - 60px);
}
</style>

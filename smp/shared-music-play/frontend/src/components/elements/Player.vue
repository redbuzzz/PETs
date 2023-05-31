<template>
  <div id="player">
  </div>
</template>

<script>
import {mapState} from "pinia";
import {useRoomStore} from "@/stores/RoomStore";

export default {
  name: "Player",
  data(){
    return {
        player: null
    }
  },
  mounted() {
  },
  methods: {
  },
  computed: {
  }
}
</script>

<style scoped>
#player {
  height: 100%;
  max-width: 100%;
}

iframe {
  width: 100%;
  height: 100%;
  border: None;
}
</style>

<template>
  <div ref="youtube"></div>
</template>

<script setup>
import {useRoomStore} from "@/stores/RoomStore";
import {ref, watch} from "vue";
import {usePlayerStore} from "@/stores/PlayerStore";
import {useWebSocketStore} from "@/stores/WebsocketStore";

const playerStore = usePlayerStore();
const roomStore = useRoomStore();
const webSocketStore = useWebSocketStore();
const youtube = ref();

playerStore.initPlayer(youtube);

const player = playerStore.player;

</script>

<style>


iframe {
  width: 100%;
  height: 100%;
  border: None;
}
</style>

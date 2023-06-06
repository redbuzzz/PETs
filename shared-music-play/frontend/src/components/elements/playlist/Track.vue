<template>
  <div class="track" :class="{active: activeTrackId === track.id}">
    <button class="close-button" @click="this.sendDeleteTrackById(track.id)">X</button>
    <img class="track-img" :src="track.thumbnail_url" :alt="track.title">
      <div class="track-description" @click="makeTrackActive">
        <a :href="track.url" class="track-title" target="_blank">
         {{ track.title }}
        </a>
      </div>
  </div>
</template>

<script>
import {mapActions, mapState, mapWritableState} from "pinia";
import {useRoomStore} from "../../../stores/RoomStore";

export default {
  props: {
    track: {
      type: Object,
      required: true
    }
  },
  computed: {
    ...mapWritableState(useRoomStore, ["activeRoom"]),
    activeTrackId() {
      return this.activeRoom.activeTrackId;
    }
  },
  methods: {
    ...mapActions(useRoomStore, ['sendDeleteTrackById']),
    makeTrackActive() {
      this.activeRoom.activeTrackId = this.track.id;
    }
  }
}
</script>

<style scoped>
  .track {
      position: relative;
      padding: 5px;
      display: flex;
      flex-direction: row;
      height: 15%;
      width: 100%;
      border: 1px solid black;
  }

  .close-button{
    position: absolute;
    top: 10px;
    right: 20px;
    width: 30px;
    height: 30px;
  }

  .track-img {
      max-width: 50%;
  }

  .track-description {
    display: flex;
    align-items: center;
    justify-content: center;
    flex: 1;
    font-family: 'Inter', sans-serif;
    font-style: normal;
    line-height: 24px;
    padding: 0 15px;
  }

  .track-title {
    color: #FFFFFF;
    font-weight: 400;
    font-size: 18px;
    text-align: center;
  }

  .active {
    background-color: #aaa;
  }
</style>

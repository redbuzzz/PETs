<template>
  <div class="search-item">
    <div class="search-item__image-wrapper">
      <img :src="thumbnail" class="full-wh search-item__image" alt="" />
    </div>
    <div class="search-item__info full-wh">
      <div class="search-item__info__row full-wh">
        <div class="search-item__title full-width">
          <a :href="link" target="_blank" v-html="title"></a>
        </div>
      </div>

      <div class="search-item__info__row full-wh">
        <div class="search-item__buttons__wrapper full-wh">
          <div class="search-item__button flex-start">
            <VideoLengthSVG />
            {{ duration }}
          </div>
          <div class="search-item__button flex-end">
            <a @click="addTrack">
              <AddToPlaylistSVG />
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import VideoLengthSVG from "@/components/svgs/VideoLengthSVG.vue";
import AddToPlaylistSVG from "@/components/svgs/AddToPlaylistSVG.vue";
import axios from "axios";
import { API_URL } from "@/services/consts";
import router from "../../router";
import {mapActions} from "pinia";
import {useRoomStore} from "../../stores/RoomStore";

export default {
  name: "SearchItem",
  data() {
    return {
      modalOpen: false,
      userRooms: [],
      selectedRoom: null,
    };
  },
  methods: {
    ...mapActions(useRoomStore, ['sendAddTrackToPlaylist']),
    addTrack() {
      this.sendAddTrackToPlaylist(this.link);
      this.$emit("addTrack")
    }
  },
  components: { AddToPlaylistSVG, VideoLengthSVG },
  props: {
    title: String,
    duration: String,
    thumbnail: String,
    link: String,
  },
};
</script>

<style scoped>
.search-item {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  margin-bottom: 10px;
  background-color: #1f1f1f;
  min-height: 250px;
  max-height: 250px;
}

.search-item * {
  color: #d9d9d9;
}

.search-item__image-wrapper {
  min-width: 450px;
  max-width: 450px;
  margin: 10px;
  overflow: hidden;
  vertical-align: center;
  justify-content: center;
}

.search-item__image {
  position: relative;
  top: -40px;
  height: 140%;
}

.search-item__info {
  display: flex;
  flex-direction: column;
}

.search-item__info__row {
  display: flex;
  align-items: center;
  justify-content: center;
}

.search-item__title {
  margin: 20px;
}

.search-item__buttons__wrapper {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.search-item__button {
  font-family: "Roboto", sans-serif;
  display: flex;
  align-items: center;
  margin: 20px;
  gap: 10px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;

  background-color: rgba(0, 0, 0, 0.5);
  z-index: 9999;

  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-container {
  background-color: #111;
  padding: 20px;
  max-width: 600px;
  width: 90%;
  text-align: center;
}

.modal-title {
  font-size: 24px;
  margin-bottom: 10px;
}

.room-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.room-list li {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px;
  background-color: #222;
  margin-bottom: 10px;
}

.add-to-playlist-button {
  background-color: #100d0d;
  color: #fff;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
}

.modal-close {
  background-color: #545454;
  color: #fff;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
}
</style>

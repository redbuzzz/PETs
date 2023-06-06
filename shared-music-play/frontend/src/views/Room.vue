<template>
  <BaseContainer>
    <MainContainer>
      <div class='main-content-block' v-if="this.activeRoomRequestData.loading">
        <Spinner :flag="this.activeRoomRequestData.loading"/>
      </div>
      <div class='main-content-block' v-else>
        <div class="modal-window" v-if="showModal">
          <div class="search-modal-window">
            <button class='close-button' @click="showModal = false">X</button>
            <InputBar placeholder="Search..." button_text="Find" v-model="this.searchString"
                      @search="this.submitSearch"/>
            <ItemsList v-if="this.videos">
              <Spinner :flag="loading"/>
              <SearchItem v-for="video in this.videos" :title="video.title" :link="video.track_url.toString()"
                          :thumbnail="video.thumbnail_url.toString()" :duration="video.duration"
                          @addTrack="showModal = false"/>
            </ItemsList>
            <div v-if="searchRequestData.loading" class="spinner-overlay">
              <div class="spinner"></div>
            </div>
            <div class="search-error" v-if="searchRequestData.error">
              {{ searchRequestData.error.message }}
            </div>
          </div>
        </div>
        <LeftContainer>
          <InputBar placeholder="Search..." button_text="Find" v-model="this.searchString" @search="this.submitSearch"/>
          <div v-if="this.activeRoom.activeTrackId" class="player-wrapper">
            <Player/>
          </div>
          <div class="player-error-handler" v-else>
            <p class="player-title"> Add any track to playlist</p>
          </div>
          <Chat/>
        </LeftContainer>
        <RightContainer>
          <div class="info">
            <p class="error" v-if="this.activeRoomRequestData.error">{{ this.activeRoomRequestData.error.message }}</p>
            <p class="loader" v-else-if="this.activeRoomRequestData.loading">Loading...</p>
          </div>

          <Playlist/>
        </RightContainer>
      </div>
    </MainContainer>
  </BaseContainer>
</template>

<script>
import BaseContainer from "@/components/containers/BaseContainer.vue";
import MainContainer from "@/components/containers/MainContainer.vue";
import RightContainer from "@/components/containers/RightContainer.vue";
import LeftContainer from "@/components/containers/LeftContainer.vue";
import Chat from "@/components/elements/Chat.vue";
import InputBar from "@/components/elements/InputBar.vue";
import Player from "@/components/elements/Player.vue";
import Playlist from "@/components/elements/playlist/Playlist.vue";
import {useRoomStore} from "@/stores/RoomStore";
import {mapActions, mapState, mapWritableState} from "pinia";
import {useWebSocketStore} from "@/stores/WebsocketStore";
import ItemsList from "../components/containers/ItemsList.vue";
import SearchItem from "../components/search/SearchItem.vue";
import {useSearchStore} from "@/stores/SearchStore";
import Spinner from "@/components/elements/Spinner.vue";

export default {
  name: "Room",
  components: {
    Spinner,
    SearchItem,
    ItemsList,
    InputBar,
    Playlist,
    Player,
    LeftContainer,
    RightContainer,
    Chat,
    MainContainer,
    BaseContainer
  },
  data() {
    return {
      showModal: false,
    }
  },
  computed: {
    ...mapWritableState(useRoomStore, ['activeRoom', 'activeRoomRequestData']),
    ...mapWritableState(useSearchStore, ["searchString", 'videos']),
    ...mapState(useSearchStore, {
      searchRequestData: "requestData",
      loading: state => state.requestData.loading,
    })
  },
  methods: {
    ...mapActions(useRoomStore, ['fetchActiveRoomData']),
    ...mapActions(useSearchStore, ["searchTracks"]),
    async submitSearch() {
      this.videos = [];
      this.showModal = true;
      await this.searchTracks();
    }
  },
  async mounted() {
    await this.fetchActiveRoomData(this.$route.params.id);
    useWebSocketStore().initWebSocket();
  }
}
</script>

<style scoped>

.modal-window {
  position: absolute;
  top: 0;
  bottom: 0;
  right: 0;
  left: 0;
}

.close-button {
  position: absolute;
  top: 5px;
  right: 5px;
  width: 30px;
  height: 30px;
}

.info {
  text-align: center;
  font-size: 25px;
  position: absolute;
  margin: 50px auto;
}

.player-error-handler {
  display: flex;
  align-items: center;
  justify-content: center;
}

.player-title {
  font-size: 36px;
  font-weight: 800;
  color: white;
}

.main-content-block {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: row;
  position: relative;
}

.error {
  color: red;
}

.loader {
  color: green;
}

.search-modal-window {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  right: 0;
  padding: 50px;
  background-color: rgba(0, 0, 0, 0.9);
  z-index: 10;
}

.player-wrapper {
  height: 100%;
}
</style>

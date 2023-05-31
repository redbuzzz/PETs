<template>
  <BaseContainer>
    <MainContainer>
      <LeftContainer>
        <form @submit.prevent="submitSearch">
            <InputBar placeholder="Search..." button_text="Find" v-model="searchQuery" @search="submitSearch"/>
        </form>
        <Player/>
        <Chat/>
      </LeftContainer>
      <RightContainer>
        <div class="info">
          <p class="error" v-if="this.activeRoomRequestData.error">{{this.activeRoomRequestData.error.message}}</p>
          <p class="loader" v-else-if="this.activeRoomRequestData.loading">Loading...</p>
        </div>

        <Playlist :playlist="this.tracks"
                  @save="this.savePlaylist"
        />
      </RightContainer>
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
import {useRoomStore} from "../stores/RoomStore";
import {mapActions, mapState, mapWritableState} from "pinia";

export default {
  name: "Room",
  components: {
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
      searchQuery: ""
    }
  },
  computed: {
    ...mapWritableState(useRoomStore, ['activeRoom', 'activeRoomRequestData']),
    tracks() {
      return (this.activeRoomRequestData.loading || this.activeRoomRequestData.error) ? [] : this.activeRoom.playlist;
    }
  },
  methods: {
    ...mapActions(useRoomStore, ['fetchActiveRoomData', 'saveActiveRoomPlaylist']),
    savePlaylist() {
      this.saveActiveRoomPlaylist();
    },
    submitSearch(query) {
      this.searchText = query;
      this.loading = false;
      this.$router.push({
        path: "/search",
        query: {q: query}
      });
    }
  },
  async mounted() {
    await this.fetchActiveRoomData(this.$route.params.id);
  }
}
</script>

<style scoped>
.info {
    text-align: center;
    font-size: 25px;
    position: absolute;
    margin: 50px auto;
}

.error {
    color: red;
}

.loader {
    color: green;
}
</style>

<template>
  <BaseContainer>
    <MainContainer>
      <LeftContainer>
        <Spinner :flag="this.roomsRequestData.loading" />
        <div id="left-block">
          <div class="title" style="text-align: left; margin: 20px 0;">
            Room
          </div>
          <SearchFilter v-model="rooms.searchString"
          />
          <RadioButtonRow :options="ROOM_OWNER_OPTIONS()" v-model="this.rooms.owner" />
          <div id="scroll-fixer">
            <ItemsList>
              <RoomLine v-for="room in getFilteredRoomList"
                        :name="room.name"
                        :id="room.id.toString()"
                        :listenerAmount="room.listener_amount"/>
              <button class="load-button" @click="loadRooms">Load more rooms</button>
            </ItemsList>
          </div>
        </div>
      </LeftContainer>
      <RightContainer>
        <HalfHeight style="margin-bottom: 10px">
          <form method="GET" id="code-form" @submit.prevent="joinRoom(roomCode)" class="full-width full-height">
            <div class="title">
              Join by code
            </div>
            <input class="big full-width" v-model="roomCode" required style="margin-bottom: 20px;"
                   placeholder="Room code...">
            <button class="big" id="join-button">Join</button>
            <div class="code-form__error"
                 v-if="this.roomJoinRequestData.error">
              {{ this.roomJoinRequestData.error.message }}
            </div>
          </form>
        </HalfHeight>
        <HalfHeight>
          <div class="title">
            Wanna listen to music with friends? Okay!
          </div>
          <button v-on:click="showModal = true" class="big">
            Create your room
          </button>
          <div class="modal-overlay" v-if="showModal">
            <ModalView @close="showModal = false"></ModalView>
          </div>
        </HalfHeight>
      </RightContainer>
    </MainContainer>
  </BaseContainer>
</template>

<script>
import BaseContainer from "@/components/containers/BaseContainer.vue";
import MainContainer from "@/components/containers/MainContainer.vue";
import LeftContainer from "@/components/containers/LeftContainer.vue";
import RightContainer from "@/components/containers/RightContainer.vue";
import SearchFilter from "@/components/elements/SearchFilter.vue";
import RoomLine from "@/components/elements/RoomLine.vue";
import HalfHeight from "@/components/elements/HalfHeight.vue";
import RoomList from "@/components/elements/RoomList.vue";
import ItemsList from "@/components/containers/ItemsList.vue";
import ModalView from "@/components/containers/ModalView.vue";
import {API_URL, ROOM_OWNER_OPTIONS, ROOM_PRIVACY_OPTIONS} from "../services/consts";
import {mapActions, mapState, mapWritableState} from "pinia";
import {useRoomStore} from "../stores/RoomStore";
import RadioButtonRow from "../components/elements/buttons/RadioButtonRow.vue";
import Spinner from "../components/elements/Spinner.vue";
import _ from "lodash";

export default {
  name: "MainPage",
  components: {
    Spinner,
    RadioButtonRow,
    ItemsList,
    RoomList,
    HalfHeight,
    RoomLine,
    SearchFilter,
    RightContainer,
    LeftContainer,
    MainContainer,
    BaseContainer,
    ModalView
  },
  mounted() {
    this.fetchRoomList();
  },
  data() {
    return {
      showModal: false,
      roomCode: "",
    }
  },
  computed: {
    ...mapWritableState(useRoomStore, ["rooms", "roomsRequestData"]),
    ...mapState(useRoomStore, ["getFilteredRoomList", "roomJoinRequestData"])
  },
  methods: {
    ROOM_OWNER_OPTIONS() {
      return ROOM_OWNER_OPTIONS
    },
    ...mapActions(useRoomStore, ["fetchRoomList", "joinRoomByCode", "fetchPublicRoomList"]),
    ROOM_PRIVACY_OPTIONS() {
      return ROOM_PRIVACY_OPTIONS;
    },
    async joinRoom(roomCode) {
      const room = await this.joinRoomByCode(roomCode);
      if (room) {
        this.$router.push({name: 'Room', params: {id: room.id}})
      }
    },
    loadRooms() {
      if (_.isEqual(this.rooms.owner, "my")) {
        this.fetchRoomList()
      } else {
        this.fetchPublicRoomList()
      }
    }
  },
  watch: {
  'rooms.owner'(newValue) {
      if (newValue === 'public') {
        this.fetchPublicRoomList()
      }
    }
  }
}
</script>

<style scoped>

.load-button {
    background-color: #3c3c3c;
    padding: 20px;
    color: #fff;
}

#scroll-fixer {
  height: 100%;
  max-height: calc(100% - 160px);
}

#left-block {
  height: 100%;
  background-color: #1F1F1F;
  padding: 20px;
  max-height: calc(100% - 40px);
}

.title {
  font-weight: 500;
  font-size: 40px;
  color: #FFFFFF;
  text-align: center;
}

#code-form {
  display: flex;
  justify-content: space-between;
  flex-direction: column;
  align-items: center;
}

#join-button {
  width: 140px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 100;
}

.code-form__error {
  color: red;
  text-align: center;
  font-size: 20px;
}

</style>

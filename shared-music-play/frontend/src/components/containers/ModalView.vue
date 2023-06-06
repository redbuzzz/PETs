<template>
    <div class="modal-view">

        <form @submit.prevent="submit" class="modal-view-content">
            <button class="close-button" @click="this.$emit('close')">X</button>
            <div class="title">
                Create your room
            </div>
            <input v-model="this.roomName" class="indent big full-width input-modal-view" required placeholder="Room name...">
            <div class="privacy">
              <RadioButtonRow
                :options="ROOM_PRIVACY_OPTIONS()"
                v-model="this.privacy"
              />
            </div>
            <button class="indent big create-button" type="submit">
                Create
            </button>
            <div class="modal-view__message">{{ this.errorMessage }}</div>
        </form>
    </div>
</template>

<script>
import {API_URL, ROOM_PRIVACY_OPTIONS} from "@/services/consts";
import {mapActions, mapState} from "pinia";
import {useRoomStore} from "@/stores/RoomStore";
import RadioButtonRow from "../elements/buttons/RadioButtonRow.vue";

export default {
  components: {RadioButtonRow},
  data() {
    return {
      roomName: "",
      formErrorMessage: "",
      privacy: null
    }
  },
  computed: {
    ...mapState(useRoomStore, ["createRoomRequestData"]),
    errorMessage() {
      if (this.createRoomRequestData.error) {
        return this.createRoomRequestData.error.message;
      }
      return this.formErrorMessage;
    }
  },
  methods: {
    ...mapActions(useRoomStore, ["createRoom"]),
    ROOM_PRIVACY_OPTIONS() {
      return ROOM_PRIVACY_OPTIONS;
    },
    async submit() {
      if (this.privacy === null) {
        this.formErrorMessage = "Choose privacy";
        return;
      }
      this.formErrorMessage = "";

      const room = await this.createRoom(this.roomName, this.privacy);

      if (room) {
        this.$router.push({name: "Room", params: {id: room.id}})
      }
    }
  }
}
</script>


<style>
.close-button{
    position: absolute;
    top: 20px;
    right: 20px;
    width: 30px;
    height: 30px;
}

.modal-view{
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-view-content{
  background: #2B2B2B;
  overflow-x: auto;
  display: flex;
  flex-direction: column;
  height: 740px;
  width: 656px;
  align-items: center;
  justify-content: center;
    position: relative;
}

.title{
  font-size: 56px;
  color: #FFFFFF;
  margin-bottom: 50px;
}

.input-modal-view{
  height: 70px;
  width: 460px;
}

.input-modal-view::placeholder{
  font-size: 32px;
  color: #2B2B2B;
}

.privacy {
    display: flex;
}

.create-button{
  width: 284px;
  height: 55px;
  background: #999999;
  font-size: 36px;
  color: #FFFFFF;
}

.indent{
  margin-top: 35px;
}

.modal-view__message {
    color: red;
}

</style>

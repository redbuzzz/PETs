<template>
  <div id="nav-bar">
    <div class="nav-top-buttons">
      <RouterLink to="/profile">
        <ProfileSVG/>
      </RouterLink>
      <RouterLink to="/main">
        <HomeSVG/>
      </RouterLink>
      <div v-if="room.id">
        <GearSVG @click="openModal" />

        <div class="modal" v-if="isModalOpen">
          <div class="modal-content">
            <div class="title-heading">
              <div class="title-room users-heading">{{ room.name }}</div>
            </div>
            <div class="room-info">
              <p class="modal-text"><strong class="modal-text">Type:</strong> {{ room.privacy }}</p>
              <p class="modal-text"><strong class="modal-text">Code:</strong> {{ room.code }}</p>
            </div>
            <div class="users-container">
              <p class="users-heading">Users:</p>
              <div v-for="user in room.users" :key="user.id" class="user-row">
                <span class="user-email modal-text">{{ user.email }}</span>
                <div v-if="getRole === 'admin'" class="user-actions">
                  <select class="dark-select" :disabled="profileInfo.id === user.id" v-model="user.room_role">
                    <option v-for="role in ROOM_ROLES()" :value="role.value" :key="role.value">{{ role.label }}</option>
                  </select>
                  <button :disabled="getRole !== 'admin'" class="dark-button" @click="updateUserRoles(user)">Save</button>
                </div>
                <div v-else class="user-actions">
                  <span class="dark-select">
                    {{ user.room_role }}
                  </span>
                </div>
              </div>
            </div>
            <div v-if="getRole === 'admin'" class="delete-button-container">
              <button class="delete-button" @click="deleteRoom">Delete Room</button>
            </div>
          </div>
          <button class="modal-close" @click="closeModal">Close</button>
        </div>
      </div>
    </div>
    <div class="nav-bottom-buttons">
      <RouterLink to="/logout">
        <LogoutSVG/>
      </RouterLink>
    </div>
  </div>
</template>

<script>
import ProfileSVG from "../svgs/ProfileSVG.vue";
import LogoutSVG from "../svgs/LogoutSVG.vue";
import HomeSVG from "../svgs/HomeSVG.vue";
import GearSVG from "../svgs/GearSVG.vue";
import {mapActions, mapState, mapWritableState} from "pinia";
import { useRoomStore } from "@/stores/RoomStore";
import { ROOM_ROLES } from "@/services/consts";
import {useUserStore} from "@/stores/UserStore";
import {useWebSocketStore} from "@/stores/WebsocketStore";

export default {
  name: "NavBar",
  components: {
    GearSVG,
    HomeSVG,
    LogoutSVG,
    ProfileSVG
  },
  data() {
    return {
      isModalOpen: false,
    };
  },
  computed: {
    ...mapWritableState(useRoomStore, {
      room: "activeRoom",
    }),
    ...mapState(useRoomStore, ['getRole']),
    ...mapState(useUserStore, ['profileInfo']),
  },
  methods: {
    ...mapActions(useUserStore, ['profileData']),
    ROOM_ROLES() {
      return ROOM_ROLES;
    },
    openModal() {
      this.isModalOpen = true;
      console.log(this.getRole)
    },
    closeModal() {
      this.isModalOpen = false;
    },
    async updateUserRoles(user) {
      useWebSocketStore().sendMessage({
        type: "update_room_role",
        data: {
          "user_id": user.id,
          "room_role": user.room_role
        }
      })
    },
    async deleteRoom() {
    }
  }
};
</script>

<style scoped>
#nav-bar {
  width: 70px;
  height: 100%;
  background-color: #1F1F1F;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: width 1s ease-in-out;
}

.nav-top-buttons, .nav-bottom-buttons {
  padding: 20px 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 10;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: #000;
  color: #fff;
  padding: 20px;
}

.modal-close {
  margin-top: 10px;
  padding: 10px 20px;
  color: #fff;
  background: #222222;
  border: 3px solid #000000;
}

.modal-text {
  color: #999999;
}

.dark-button {
  background-color: #1F1F1F;
  color: #fff;
  padding: 5px 10px;
  margin: 5px;
  cursor: pointer;
  border: 1px solid #3C3C3C;
}

.dark-select {
  background-color: #1F1F1F;
  color: #fff;
  padding: 5px 10px;
  margin: 5px;
  border: 1px solid #3C3C3C;
}

.room-info {
  margin-bottom: 25px;
}

.users-container {
  margin-bottom: 20px;
}

.users-heading {
  color: #fff;
  font-weight: bold;
  margin-bottom: 10px;
}

.user-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.user-email {
  margin-right: 10px;
}

.delete-button {
  background-color: #545454;
  color: #fff;
  padding: 5px 10px;
  margin-top: 20px;
  cursor: pointer;
  border: 1px solid #100d0d;
}

.delete-button-container, .title-heading {
  display: flex;
  justify-content: center;
}

.title-heading {
  margin-bottom: 20px;
}

.title-room {
  font-size: 36px;
}

.user-actions {
  display: flex;
  align-items: center;
}
</style>

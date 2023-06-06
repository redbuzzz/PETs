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
          <div class="modal-content" v-if="isBanFormOpen">
            <form @submit.prevent="this.submitBan" class="ban-form">
              <p class="modal-text">
                Ban user {{ this.banFormUser.name }}
              </p>
              <InputBlock name="ban_until"
                          v-model="banUntil"
                          label="Ban until (leave empty if permanent)"
                          type="datetime-local"
                          :required="false" />
              <button class="dark-button">Ban</button>
            </form>
          </div>

          <div class="modal-content" v-else>
            <div class="title-heading">
              <div class="title-room users-heading">{{ room.name }}</div>
            </div>
            <div class="room-info">
              <p class="modal-text"><strong class="modal-text">Type:</strong> {{ room.privacy }}</p>
              <p class="modal-text"><strong class="modal-text">Code:</strong> {{ room.code }}</p>
            </div>
            <div class="tab-row">
              <button class="tab-button dark-button"
                      :class="{active: activeTab === 'users'}"
                      @click="this.activeTab='users'">
                Users
              </button>
              <button class="tab-button dark-button"
                      :class="{active: activeTab === 'bans'}"
                      v-if="getRole === 'admin' || getRole === 'moderator'"
                      @click="this.activeTab='bans'">
                Bans
              </button>
            </div>
            <div class="tab" v-if="this.activeTab === 'users'">
              <p class="users-heading">Users:</p>
              <div v-for="user in room.users" :key="user.id" class="user-row">
                <span class="user-email modal-text">{{ user.name }} ({{ user.email }})</span>
                <div v-if="getRole === 'admin' || getRole === 'moderator'" class="user-actions">
                  <select class="dark-select" :disabled="profileInfo.id === user.id || getRole !== 'admin'" v-model="user.room_role">
                    <option v-for="role in ROOM_ROLES()" :value="role.value" :key="role.value">{{ role.label }}</option>
                  </select>
                  <button v-if="getRole === 'admin'" class="dark-button" @click="updateUserRoles(user)">Save</button>
                  <button class="dark-button" :disabled="profileInfo.id === user.id" @click="this.showBanForm(user)">Ban</button>
                </div>
                <div v-else class="user-actions">
                  <span class="dark-select">
                    {{ getRoomRoleLabel(user.room_role) }}
                  </span>
                </div>
              </div>
            </div>
            <div class="tab" v-if="this.activeTab === 'bans'">
              <Spinner :flag="this.activeRoomBansRequestData.loading" />
              <p class="users-heading">Banned users:</p>
              <div v-for="ban in this.room.bans" class="ban-item">
                <div class="ban-left">
                  <p class="modal-text">
                    {{ ban.user.name }} ({{ ban.user.email }})
                  </p>
                  <p class="modal-text">Banned on {{ this.getFormattedDate(ban.banned_at) }}</p>
                  <p v-if="ban.banned_until" class="modal-text">Banned until
                    {{ this.getFormattedDate(ban.banned_until) }}</p>
                  <p v-else class="modal-text">Banned permanently</p>
                </div>
                <div class="ban-right">
                  <button class="dark-button" @click="this.submitUnban(ban.user)">Unban</button>
                </div>
              </div>
            </div>
            <div v-if="getRole === 'admin'" class="delete-button-container">
              <button class="delete-button" @click="confirmDeleteRoom">Delete Room</button>
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
import Spinner from "./Spinner.vue";
import moment from "moment";
import _ from "lodash";
import InputBlock from "./auth/InputBlock.vue";

export default {
  name: "NavBar",
  components: {
    InputBlock,
    Spinner,
    GearSVG,
    HomeSVG,
    LogoutSVG,
    ProfileSVG
  },
  data() {
    return {
      isModalOpen: false,
      activeTab: "users",
      banFormUser: null,
      isBanFormOpen: false,
      banUntil: null,
      isBanPermanent: false
    };
  },
  computed: {
    ...mapWritableState(useRoomStore, {
      room: "activeRoom",
    }),
    ...mapState(useRoomStore, ['getRole', 'activeRoomBansRequestData']),
    ...mapState(useUserStore, ['profileInfo']),
  },
  methods: {
    ...mapActions(useUserStore, ['profileData']),
    ...mapActions(useRoomStore, ['fetchActiveRoomBans', 'sendBanUser', 'sendUnbanUser', 'sendDeleteRoom']),
    ROOM_ROLES() {
      return ROOM_ROLES;
    },
    openModal() {
      this.isModalOpen = true;
    },
    closeModal() {
      this.isModalOpen = false;
      this.closeBanForm();
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
    async confirmDeleteRoom() {
      const res = confirm("Are you sure you want to delete this room?");
      if (res) {
        this.sendDeleteRoom();
      }
    },
    getFormattedDate(date) {
      return moment(date).format("YYYY-MM-DD, hh:mm")
    },
    getRoomRoleLabel(role) {
      return _.find(ROOM_ROLES, {value: role}).label
    },
    showBanForm(user) {
      this.banFormUser = user;
      this.isBanFormOpen = true;
    },
    closeBanForm() {
      this.isBanFormOpen = false;
    },
    submitBan() {
      console.log("BANNING", this.banFormUser)
      this.sendBanUser(this.banFormUser, this.banUntil);
      this.closeBanForm();
    },
    submitUnban(user) {
      this.sendUnbanUser(user);
    }
  },
  watch: {
    async activeTab(newValue) {
      if (newValue === 'bans') {
        await this.fetchActiveRoomBans();
      }
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
  min-width: 700px;
  min-height: 500px;
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

.tab-row {
  display: flex;
  justify-content: center;
}

.tab {
  margin-bottom: 20px;
}

.tab-button.active {
  background-color: #777;
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

.ban-item {
  border-top: 1px solid #fff;
  border-bottom: 1px solid #fff;
  padding: 5px 0;
  display: flex;
  justify-content: space-between;
}

.ban-form {
  padding: 50px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>

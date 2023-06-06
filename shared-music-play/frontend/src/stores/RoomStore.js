import {defineStore} from "pinia";
import _ from "lodash";
import {useChatStore} from "@/stores/ChatStore";
import {useWebSocketStore} from "./WebsocketStore";
import {apiCreateRoom, apiFetchActiveRoom, apiFetchRooms, apiJoinRoom, apiFetchActiveRoomBans, apiFetchPublicRooms} from "@/services/api";
import {useUserStore} from "./UserStore";
import moment from "moment";
import router from "../router";
import {ROOM_OWNER_OPTIONS} from "../services/consts";


export const useRoomStore = defineStore({
  id: 'roomStore',
  state: () => ({
    activeRoom: {
      id: null,
      name: null,
      code: null,
      privacy: null,
      playlist: [],
      users: [],
      bans: [],
      activeTrackId: null
    },
    rooms: {
      list: [],
      listLimit: 5,
      publicList: [],
      publicListLimit: 5,
      searchString: "",
      owner: ROOM_OWNER_OPTIONS[0].value,
    },
    activeRoomRequestData: {
      loading: false,
      error: null,
    },
    activeRoomBansRequestData: {
      loading: false,
      error: null,
    },
    playlistRequestData: {
      loading: false
    },
    roomsRequestData: {
      loading: false,
      error: null,
    },
    roomJoinRequestData: {
      loading: false,
      error: null,
    },
    createRoomRequestData: {
      loading: false,
      error: null,
    },
  }),
  actions: {
    async fetchActiveRoomData(id) {
      this.activeRoomRequestData.loading = true;
      this.activeRoomRequestData.error = null;
      try {
        const roomData = await apiFetchActiveRoom(id);

        this.activeRoom.id = roomData.id;
        this.activeRoom.playlist = roomData.playlist;
        this.activeRoom.activeTrackId = (roomData.playlist.length === 0) ? null : roomData.playlist[0].id;
        this.activeRoom.users = roomData.users;
        this.activeRoom.privacy = roomData.privacy;
        this.activeRoom.code = roomData.code;
        this.activeRoom.name = roomData.name;

        const {messages} = roomData;
        useChatStore().cleanMessages();
        useChatStore().fillMessages(messages);
      } catch (error) {
        this.activeRoomRequestData.error = error;
      }
      this.activeRoomRequestData.loading = false;
    },
    async fetchActiveRoomBans() {
      this.activeRoomBansRequestData.loading = true;
      this.activeRoomBansRequestData.error = null;

      try {
        this.activeRoom.bans = await apiFetchActiveRoomBans(this.activeRoom.id)
      } catch (e) {
        this.activeRoomBansRequestData.error = e;
      }

      this.activeRoomBansRequestData.loading = false;
    },
    async fetchRoomList() {
      this.roomsRequestData.loading = true;
      this.roomsRequestData.error = null;
      try {
        const data = await apiFetchRooms(this.rooms.listLimit, this.listOffset);
        this.rooms.list = this.rooms.list.concat(data.results);
      } catch (error) {
        this.error = error;
      }
      this.roomsRequestData.loading = false;
    },
    async fetchPublicRoomList() {
      this.roomsRequestData.loading = true;
      this.roomsRequestData.error = null;
      try {
        const data = await apiFetchPublicRooms(this.rooms.publicListLimit, this.publicListOffset);
        this.rooms.publicList = this.rooms.publicList.concat(data.results);
      } catch (error) {
        this.error = error;
      }
      this.roomsRequestData.loading = false;
    },
    async joinRoomByCode(code) {
      this.roomJoinRequestData.loading = true;
      this.roomJoinRequestData.error = null;

      try {
        const newRoom = await apiJoinRoom(code);
        this.rooms.list.push(newRoom);
        return newRoom;
      } catch (error) {
        this.roomJoinRequestData.error = error;
      }

      this.roomJoinRequestData.loading = false;
    },
    async createRoom(name, privacy) {
      this.createRoomRequestData.error = null;
      this.createRoomRequestData.loading = true;

      try {
        const newRoom = await apiCreateRoom(name, privacy);
        this.rooms.list.push(newRoom);
        return newRoom;
      } catch (error) {
        this.createRoomRequestData.error = error;
      }

      this.createRoomRequestData.loading = false;
    },
    previousTrack() {
      let index = _.max([0, this.getActiveTrackIndex - 1]);
      this.activeRoom.activeTrackId = this.activeRoom.playlist[index].id;
    },
    nextTrack() {
      if (this.activeRoom.activeTrackId) {
        let index = _.min([this.getActiveTrackIndex + 1, this.activeRoom.playlist.length - 1]);
        this.activeRoom.activeTrackId = this.activeRoom.playlist[index].id;
      }

    },
    clearActiveRoom() {
      this.activeRoom.id = null;
    },
    clearRooms(){
      this.rooms.list = [];
      this.rooms.publicList = [];
    },
    changeUserRole(userId, room_role) {
      _.find(this.activeRoom.users, (user) => user.id === userId).room_role = room_role;
    },
    addUser(user){
      let index = _.findIndex(this.activeRoom.users, {id: user.id});
      if (index === -1) {
        this.activeRoom.users.push(user);
      } else {
        this.activeRoom.users[index] = user;
      }
    },
    sendUpdatePlaylistOrder() {
      this.playlistRequestData.loading = true;
      const playlistIds = this.activeRoom.playlist.map(track => track.id);

      useWebSocketStore().sendMessage({
        type: "playlist_order",
        data: {
          activeTrackId: this.activeRoom.activeTrackId,
          playlist: playlistIds
        }
      })
    },
    updatePlaylistOrder(data) {
      this.activeRoom.activeTrackId = data.activeTrackId;
      this.activeRoom.playlist.sort(function (a, b) {
        return data.playlist.indexOf(a.id) - data.playlist.indexOf(b.id);
      });
      for (let i in this.activeRoom.playlist) {
        this.activeRoom.playlist[i].order_num = i;
      }
      this.playlistRequestData.loading = false;
    },
    sendAddTrackToPlaylist(trackUrl) {
      useWebSocketStore().sendMessage({
        type: "add_track",
        data: {
          link: trackUrl
        }
      })
    },
    addTrackToPlaylist(track) {
      this.activeRoom.playlist.push(track);
      if (this.activeRoom.playlist.length === 1) {
        useRoomStore().activeRoom.activeTrackId = this.activeRoom.playlist[0].id;
      }
    },
    sendDeleteTrackById(id) {
      useWebSocketStore().sendMessage({
        type: "delete_track",
        data: {
          id: id
        }
      })
    },
    deleteTrackById(id) {
      const playlist = this.activeRoom.playlist;
      if (playlist.length === 1) {
        this.clearPlaylist();
        return;
      }
      if (id === this.activeRoom.activeTrackId) {
        if (this.isActiveTrackLast) {
          this.previousTrack();
        } else {
          this.nextTrack()
        }
      }
      this.activeRoom.playlist = _.filter(playlist, (track) => track.id !== id);
    },
    sendClearPlaylist() {
      useWebSocketStore().sendMessage({
        type: "clear_playlist",
        data: {}
      })
    },
    clearPlaylist() {
      this.activeRoom.activeTrackId = null;
      this.activeRoom.playlist = [];
    },
    sendBanUser(user, banUntil) {
      useWebSocketStore().sendMessage({
        type: "ban",
        data: {
          "user_id": user.id,
          "ban_until": banUntil
        }
      })
    },
    banUser(userId, bannedUntil) {
      if (useUserStore().profileInfo.id === userId) {
        let bannedUntilString = (bannedUntil === null) ? "permanently" : `until ${moment(bannedUntil, "dd-mm-yyyy")}`;
        alert(`Oops! You were banned ${bannedUntilString}`)
        router.push({name: 'Main'});
      }
      this.activeRoom.users = _.filter(this.activeRoom.users, (obj) => obj.id !== userId);
    },
    sendUnbanUser(user) {
      useWebSocketStore().sendMessage({
        type: "unban",
        data: {
          "user_id": user.id
        }
      })
    },
    unbanUser(userId) {
      this.activeRoom.bans = _.filter(this.activeRoom.bans, (obj) => obj.user.id !== userId);
    },
    sendDeleteRoom() {
      useWebSocketStore().sendMessage({
        type: "delete_room",
        data: {}
      })
    },
    deleteRoom() {
      alert("Oh no! This room was deleted!");
      router.push({name: "Main"});
    }
  },
  getters: {
    getFilteredRoomList() {
      const lst = this.rooms.owner === ROOM_OWNER_OPTIONS[0].value ? this.rooms.list : this.rooms.publicList;
      return _.filter(lst, (room) => {
          return room.name.toLowerCase().indexOf(this.rooms.searchString.toLowerCase()) !== -1
      });
    },
    getActiveTrack() {
      if (this.getActiveTrackIndex === -1) {
        return null;
      }
      return this.activeRoom.playlist[this.getActiveTrackIndex];
    },
    getActiveTrackIndex() {
      return _.findIndex(this.activeRoom.playlist, (track) => track.id === this.activeRoom.activeTrackId)
    },
    getRole() {
      for (const user of this.activeRoom.users) {
        if (useUserStore().profileInfo.id === user.id) {
          return user.room_role;
        }
      }
    },
    isActiveTrackLast() {
      return this.getActiveTrackIndex === this.activeRoom.playlist.length - 1
    },
    listOffset() {
      return this.rooms.list.length;
    },
    publicListOffset() {
      return this.rooms.publicList.length;
    }
  }
})

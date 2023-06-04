import {defineStore} from "pinia";
import _ from "lodash";
import {useChatStore} from "@/stores/ChatStore";
import {useWebSocketStore} from "./WebsocketStore";
import {apiCreateRoom, apiFetchActiveRoom, apiFetchRooms, apiJoinRoom, apiUpdateRoomRole} from "@/services/api";
import {useUserStore} from "./UserStore";


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
      activeTrackId: null
    },
    rooms: {
      list: [],
      searchString: "",
      privacyFilters: [],
    },
    activeRoomRequestData: {
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
    saveActiveRoomPlaylistOrder() {
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
    addTrackToPlaylist(trackUrl) {
      useWebSocketStore().sendMessage({
        type: "add_track",
        data: {
          link: trackUrl
        }
      })
    },
    updateActiveRoomPlaylistOrder(data) {
      this.activeRoom.activeTrackId = data.activeTrackId;
      this.activeRoom.playlist.sort(function (a, b) {
        return data.playlist.indexOf(a.id) - data.playlist.indexOf(b.id);
      });
      for (let i in this.activeRoom.playlist) {
        this.activeRoom.playlist[i].order_num = i;
      }
      this.playlistRequestData.loading = false;
    },
    async fetchRoomList() {
      this.roomsRequestData.loading = true;
      this.roomsRequestData.error = null;
      try {
        const data = await apiFetchRooms();
        this.rooms.list = data;
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
    changeUserRole(userId, room_role) {
      _.find(this.activeRoom.users, (user) => user.id === userId).room_role = room_role;
    },
    websocketDeleteTrackById(id) {
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
    websocketClearPlaylist() {
      useWebSocketStore().sendMessage({
        type: "clear_playlist",
        data: {}
      })
    },
    clearPlaylist() {
      this.activeRoom.activeTrackId = null;
      this.activeRoom.playlist = [];
    }
  },
  getters: {
    getFilteredRoomList() {
      return this.rooms.list.filter((room) => {
          return room.name.toLowerCase().indexOf(this.rooms.searchString.toLowerCase()) !== -1 &&
              (_.some(this.rooms.privacyFilters, {"value": room.privacy}) || this.rooms.privacyFilters.length === 0);
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
    }
  }
})

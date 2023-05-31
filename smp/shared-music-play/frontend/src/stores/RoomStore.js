import {defineStore} from "pinia";
import _ from "lodash";
import {apiCreateRoom, apiFetchActiveRoom, apiFetchRooms, apiJoinRoom, apiSavePlaylist} from "@/services/api";

export const useRoomStore = defineStore({
  'id': 'roomStore',
  state: () => ({
    activeRoom: {
      id: undefined,
      playlist: [],
    },
    rooms: {
      list: [],
      searchString: "",
      privacyFilters: [],
    },
    activeRoomRequestData: {
      loading: false,
      error: null
    },
    roomsRequestData: {
      loading: false,
      error: null
    },
    roomJoinRequestData: {
      loading: false,
      error: null
    },
    createRoomRequestData: {
      loading: false,
      error: null
    }
  }),
  actions: {
    async fetchActiveRoomData(id) {
      this.activeRoomRequestData.loading = true;
      this.activeRoomRequestData.error = null;
      try {
        const data = await apiFetchActiveRoom(id);
        this.activeRoom = data;
      } catch (error) {
        this.activeRoomRequestData.error = error;
      }
      this.activeRoomRequestData.loading = false;
    },
    async saveActiveRoomPlaylist() {
      this.activeRoomRequestData.error = null;
      this.activeRoomRequestData.loading = true;
      const playlistIds = this.activeRoom.playlist.map(track => track.id);

      try {
        await apiSavePlaylist(this.activeRoom.id, playlistIds);

        this.activeRoom.playlist.forEach((track, index) => {
          track.order_num = index;
        })
      } catch (error) {
        this.activeRoomRequestData.error = error;
        this.activeRoom.playlist.sort((a, b) => a.order_num - b.order_num);
      }

      this.activeRoomRequestData.loading = false;
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
    }
  },
  getters: {
    getFilteredRoomList() {
      return this.rooms.list.filter((room) => {
          return room.name.toLowerCase().indexOf(this.rooms.searchString.toLowerCase()) !== -1 &&
              (_.some(this.rooms.privacyFilters, {"value": room.privacy}) || this.rooms.privacyFilters.length === 0);
      });
    }
  }
})

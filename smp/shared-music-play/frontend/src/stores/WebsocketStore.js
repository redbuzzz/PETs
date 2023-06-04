import {defineStore} from "pinia";
import {WEBSOCKET_URL} from "@/services/consts";
import {useUserStore} from "@/stores/UserStore";
import {usePlayerStore} from "@/stores/PlayerStore";
import {useRoomStore} from "@/stores/RoomStore";
import {useChatStore} from "@/stores/ChatStore";
import {usePlayer} from "@vue-youtube/core";

export const useWebSocketStore = defineStore("webSocketStore", {
  state: () => ({
    webSocket: null,
  }),
  actions: {
    sendMessage(message) {
      console.log("SENDING", message)
      this.webSocket.send(JSON.stringify(message));
    },
    initWebSocket() {
      this.webSocket = new WebSocket(`${WEBSOCKET_URL}/room/${useRoomStore().activeRoom.id}?token=${useUserStore().token}`);
      this.webSocket.onmessage = this.onMessage;
      this.webSocket.onopen = this.onOpen;

    },
    onMessage(event) {
      const message = JSON.parse(event.data);
      const {type} = message;
      const {data} = message;
      console.log("RECEIVING", message)
      switch (type) {
        case "player":
          usePlayerStore().updatePlayerState(data);
          break
        case "player_request":
          const new_data = usePlayerStore().getPlayerState();
          if (new_data !== null) {
            const new_message = {
              type: "player_init",
              data: new_data
            }
            this.sendMessage(new_message)
          }
          break
        case "player_init":
          if (!usePlayerStore().isReady) {
            usePlayerStore().player.onReady(event => {
              usePlayerStore().updatePlayerState(data);
              usePlayerStore().isReady = true;
              // usePlayerStore().player.instance.unMute();
            })
          }
          break
        case "playlist_order":
          useRoomStore().updateActiveRoomPlaylistOrder(data)
          break
        case "add_track":
          const playlist = useRoomStore().activeRoom.playlist;
          playlist.push(data.track);
          if (playlist.length === 1) {
            useRoomStore().activeRoom.activeTrackId = playlist[0].id;
          }
          break;
        case "chat":
          useChatStore().messages.push(data)
          console.log('adding to chat')
          break;
        case "update_room_role":
          useRoomStore().changeUserRole(data['user_id'], data['room_role']);
          break;
        case "delete_track":
          useRoomStore().deleteTrackById(data['id'])
          break;
        case "clear_playlist":
          useRoomStore().clearPlaylist();
          break;
      }
    },
    onOpen(event) {
      const message = {
        type: 'player_request'
      };
      this.sendMessage(message);
    },
    closeConnection(){
      this.webSocket.close();
    }
  }
})

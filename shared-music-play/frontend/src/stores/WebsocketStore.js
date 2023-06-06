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
      const {type, data} = message;
      console.log("RECEIVING", message)
      switch (type) {
        case "player":
          usePlayerStore().updatePlayerState(data);
          break
        case "player_request":
          usePlayerStore().sendPlayerInit()
          break
        case "player_init":
          usePlayerStore().playerInit(data);
          break
        case "playlist_order":
          useRoomStore().updatePlaylistOrder(data)
          break
        case "add_track":
          useRoomStore().addTrackToPlaylist(data.track)
          break;
        case "chat":
          useChatStore().messages.push(data)
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
        case "ban":
          useRoomStore().banUser(data['user_id'], data['ban_until']);
          break;
        case "unban":
          useRoomStore().unbanUser(data['user_id']);
          break;
        case "delete_room":
          useRoomStore().deleteRoom();
          break;
        case "user":
          useRoomStore().addUser(data["user"]);
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

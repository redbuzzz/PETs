import {defineStore} from "pinia";
import {useWebSocketStore} from "@/stores/WebsocketStore";
import {useUserStore} from "@/stores/UserStore";
import {useRoomStore} from "@/stores/RoomStore";

export const useChatStore = defineStore('chatStore', {
  state: () => ({
    messages: []
  }),
  actions: {
    sendMessage(messageText) {
      const now = new Date();
      const time = now.toLocaleTimeString();
      useWebSocketStore().sendMessage(
        {
          type: 'chat',
          data: {
            'text': messageText,
            'time': time
          }
        }
      )
    },
    cleanMessages() {
      this.messages = [];
    },
    fillMessages(messages) {
      for (const message of messages) {
        const userId = message.user_id;
        const time = new Date(message.created_at);
        const timeString = time.toLocaleTimeString();
        const username = useRoomStore().activeRoom.users.find((user) => {
          if (user.id === userId) {
            return true
          }
        })?.name || "Unknown name";
        this.messages.push({
          text: message.text,
          username: username,
          time: timeString
        })
      }
    }
  },
  getters: {}
})

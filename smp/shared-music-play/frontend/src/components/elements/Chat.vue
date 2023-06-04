<template>
  <div class="chat">
      <div class="chat-log" v-scroll-bottom>
        <ChatMessage v-for="message in messages"
                     :time="message.time"
                     :username="message.username"
                     :text="message.text"/>
      </div>
    <div class="chat-input-bar">
      <InputBar :placeholder="'Type a message...'" :button_text="'Send'" @search="sendMessage" v-model="chatMessage"/>
    </div>
  </div>
</template>

<script>
import InputBar from "@/components/elements/InputBar.vue";
import {useChatStore} from "@/stores/ChatStore";
import ChatMessage from "@/components/elements/ChatMessage.vue";
import {mapState} from "pinia";

export default {
  name: "Chat",
  components: {ChatMessage, InputBar},
  data() {
    return {
      chatMessage: '',
    }
  },
  methods: {
    sendMessage() {
      useChatStore().sendMessage(this.chatMessage);
      this.chatMessage = '';
    }
  },
  computed: {
    ...mapState(useChatStore, ['messages'])
  },
  directives: {
    'scroll-bottom': {
      mounted: function (el) {
        el.scrollTop = el.scrollHeight;
      },
      updated: function (el) {
        el.scrollTop = el.scrollHeight;
      }
    }
  },
}
</script>

<style scoped>
.chat {
  width: 100%;
  height: 240px;
  background-color: #1F1F1F;
  display: flex;
  flex-direction: column;
  margin-top: 10px;
  position: relative;
  z-index: 3;
}


.chat-log {
  width: 100%;
  height: 100%;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.chat-input-bar {
  width: 100%;
  height: 45px;
}

.chat-input-bar form {
  display: flex;
  flex-direction: row;
  width: 100%;
}


</style>

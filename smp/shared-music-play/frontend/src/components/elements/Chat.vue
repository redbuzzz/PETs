<template>
  <div class="chat">
    <div class="chat-log"></div>
    <div class="chat-input-bar">
      <InputBar :placeholder="'Type a message...'" :button_text="'Send'"/>
    </div>
  </div>
</template>

<script>
import InputBar from "@/components/elements/InputBar.vue";

export default {
  name: "Chat",
  components: {InputBar}
}
</script>

<style scoped>
.chat {
  width: 100%;
  height: 240px;
  background-color: #1F1F1F;
  display: flex;
  flex-direction: column;
}

.chat-log {
  width: 100%;
  height: 100%;
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

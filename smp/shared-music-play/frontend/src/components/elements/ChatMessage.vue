<template>
  <div class="message">
    <div class="user-info">
      <p class="username">{{ username }}</p>
      <p class="time"> {{ time }}</p>
    </div>
    <div>
      <p class="message-text">{{ text }}</p>
    </div>
  </div>

</template>

<script>
export default {
  name: "ChatMessage",
  props: {
    text: String,
    time: String,
    username: String
  }
}
</script>

<style scoped>
.message{
  display: flex;
  flex-direction: column;
  justify-content: left;
  padding: 7px;
  border: 1px solid rgba(43, 43, 43, .7);

}
.user-info{
  display: flex;
  flex-direction: row;
  align-items: center;

}

.username{
  font-size: 16px;
  color: #d8d8d8;
}
.time{
  font-size: 14px;
  color: #a2a2a2;
  margin-left: 5px;
}
.message-text{
  font-size: 16px;
  color: white;
  overflow-wrap: break-word;
  max-width: 100%;
}

</style>
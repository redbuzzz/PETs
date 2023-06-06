<template>
    <RouterLink :to="roomLink" class="room-line full-width big">
        <div class="room-name">
            {{ name }}
        </div>
        <div class="listener-count">
            {{ listenerAmount }} listeners
        </div>
    </RouterLink>
</template>

<script>
export default {
  name: "RoomLine",
  props: {
      id: {type: String, required: true},
      name: {type: String, required: true},
      listenerAmount: {type: Number, default: 0}
  },
  computed: {
   roomLink() {
       return {name: 'Room', params: {id: this.id}};
   }
  }
}
</script>

<style scoped>
.room-line {
  display: flex;
  flex-direction: row;
  background-color: #4F4F4F4F;
  align-items: center;
  margin-bottom: 10px;
  min-height: 55px;
  max-height: 55px;
}

.room-name {
  margin-left: 50px;
  color: #FFFFFF;
  font-weight: 400;
}

.listener-count {
  margin-left: auto;
  margin-right: 50px;
  color: #FFFFFF;
  font-weight: 400;
}

</style>

<template>
  <div class="playlist">
    <draggable :list="this.playlist"
               item-key="url"
               group="playlist">

      <template #item="{element}">
        <Track :track="element" />
      </template>

    </draggable>

  </div>
  <div class="playlist-buttons">
    <button class="small white-bg full-width">Clear</button>
    <button class="small gray-bg full-width" @click="this.$emit('save')">Save</button>
  </div>
</template>

<script>
import draggable from 'vuedraggable';
import Track from "./Track.vue";

export default {
  name: "Playlist",
  components: {Track, draggable},
  props: {
    playlist: {
      type: Array,
      required: true
    }
  }
}
</script>

<style scoped>
.playlist {
  width: 100%;
  height: 100%;
  background-color: #1F1F1F;
  overflow-y: auto;
  overflow-x: hidden;
}

.playlist-buttons {
  height: 45px;
  display: flex;
  flex-direction: row;
}
</style>

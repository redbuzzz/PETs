<template>
  <div class="track">
    <img class="track-img" :src="track.thumbnail_url" :alt="track.title">
      <div class="track-description">
        <a :href="track.url" class="track-title" target="_blank">
         {{ track.title }}
        </a>
      </div>
  </div>
</template>

<script>
export default {
  props: {
    track: {
      type: Object,
      required: true
    }
  }
}
</script>

<style>
  .track {
      padding: 5px;
      display: flex;
      flex-direction: row;
      height: 15%;
      width: 100%;
      border: 1px solid black;
  }

  .track-img {
      max-width: 50%;
  }

  .track-description {
    display: flex;
    align-items: center;
    justify-content: center;
    flex: 1;
    font-family: 'Inter', sans-serif;
    font-style: normal;
    line-height: 24px;
    padding: 0 15px;
  }

  .track-title {
    color: #FFFFFF;
    font-weight: 400;
    font-size: 18px;
    text-align: center;
  }
</style>

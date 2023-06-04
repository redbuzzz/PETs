import {defineStore} from "pinia";
import {PlayerState, usePlayer} from "@vue-youtube/core";
import {useRoomStore} from "./RoomStore";
import {computed, ref, watch} from "vue";
import {useWebSocketStore} from "./WebsocketStore";

export const usePlayerStore = defineStore('playerStore', () => {
  const player = ref(null);
  const isReady = ref(false);
  const shouldSendData = ref(true);

  function initPlayer(elementRef) {
    player.value = usePlayer(getCurrentVideoId, elementRef, {
      cookie: false,
      playerVars: {
        mute: 1,
      },
    })

    player.value.onStateChange((event) => {
      console.log("PLAYER STATE CHANGE", event.target.getPlayerState(), event.target)
      const data = getPlayerState();

      if (data.currentState === PlayerState.ENDED) {
        useRoomStore().nextTrack();
      }

      if (shouldSendData.value && [PlayerState.PAUSED, PlayerState.PLAYING].includes(data.currentState)) {
        useWebSocketStore().sendMessage({
          type: "player",
          data: data
        });
      }
    });
  }
  function updatePlayerState(data) {
    console.log("UPDATING PLAYER", data)
    setShouldSendData(false)

    if (data.activeTrackId) {
      updateActiveTrack(data.activeTrackId);

      setTimeout(() => {

        updatePlayerTimeAndPlayingState(data);
        setShouldSendData(true)

      }, 1000)

    } else {
      updatePlayerTimeAndPlayingState(data);
      setShouldSendData(true)
    }
  }

  function setShouldSendData(value) {
    if (value) {
      setTimeout(() => {
        shouldSendData.value = true;
      }, 1000) // or else handler will work
    } else {
      shouldSendData.value = false;
    }
  }

  function updateActiveTrack(activeTrackId) {
    useRoomStore().activeRoom.activeTrackId = activeTrackId;
  }

  function updatePlayerTimeAndPlayingState(data) {

    if (data.currentTime) {
      player.value.instance.seekTo(data.currentTime, true);
    }
    switch (data.currentState) {
      case PlayerState.PLAYING:
        player.value.instance.playVideo();
        break
      case PlayerState.PAUSED:
        player.value.instance.pauseVideo();
        break
    }
  }

  function getPlayerState() {
    return {
      currentState: player.value.instance.getPlayerState(),
      currentTime: player.value.instance.getCurrentTime(),
      activeTrackId: useRoomStore().activeRoom.activeTrackId,
    }
  }

  function getVideoIdFromUrl(url) {
    url = url.split(/(vi\/|v=|\/v\/|youtu\.be\/|\/embed\/)/);
    return (url[2] !== undefined) ? url[2].split(/[^0-9a-z_\-]/i)[0] : url[0];
  }
  const getCurrentVideoId = computed(() => {
    const activeTrack = useRoomStore().getActiveTrack;
    return (activeTrack === null) ? null : getVideoIdFromUrl(activeTrack.link);
  })

  return {
    player,
    isReady,
    getPlayerState,
    updatePlayerState,
    initPlayer,
    getCurrentVideoId
  }
})

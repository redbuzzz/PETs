import {defineStore} from "pinia";
import {apiSearchVideo} from "../services/api";

export const useSearchStore = defineStore("searchStore", {
  state: () => ({
    videos: [],
    searchString: "",
    requestData: {
      loading: false,
      error: null
    }
  }),
  actions: {
    async searchTracks() {
      this.requestData.loading = true;
      try {
        this.videos = await apiSearchVideo(this.searchString);
      } catch (e) {
        this.requestData.error = e;
      }
      this.requestData.loading = false;
    }
  }
})

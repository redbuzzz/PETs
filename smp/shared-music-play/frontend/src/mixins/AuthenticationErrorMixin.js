import {mapState} from "pinia";
import {useUserStore} from "@/stores/UserStore";

export default {
  computed: {
    ...mapState(useUserStore, {
      authError: "error"
    }),
    error() {
      if (this.authError) {
        return `Error ${this.authError.response.status || "unknown"}`;
      }
      return null;
    }
  }
}

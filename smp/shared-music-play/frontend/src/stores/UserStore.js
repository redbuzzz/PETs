import {defineStore} from "pinia";
import {apiLogin, apiRegister} from "../services/api";

export const useUserStore = defineStore({
  id: "userStore",
  state: () => ({
    token: null,
    error: null,
    loading: false
  }),
  actions: {
    async login(email, password) {
      this.loading = true;
      this.error = null;
      try {
        const data = await apiLogin(email, password);
        this.setToken(data.token);
      } catch (error) {
        this.error = error;
      }
      this.loading = false;
    },
    async register(email, password) {
      this.loading = true;
      this.error = null;
      try {
        const data = await apiRegister(email, password);
        this.setToken(data.token);
      } catch (error) {
        this.error = error;
      }
      this.loading = false;
    },
    setToken(token) {
      this.token = token;
      localStorage.setItem("token", token);
    },
    clearError() {
      this.error = null;
    },
    getToken() {
      if (!this.token) {
        this.token = localStorage.getItem("token");
      }
      return this.token;
    },
  },
})

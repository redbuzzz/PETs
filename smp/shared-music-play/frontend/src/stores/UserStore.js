import {defineStore} from "pinia";
import {apiLogin, apiProfileData, apiRegister, apiUpdateProfile} from "@/services/api";
import {getToken, storeToken} from "@/services/localData";

export const useUserStore = defineStore({
  id: "userStore",
  state: () => ({
    requestData: {
      error: null,
      loading: false,
    },
    token: getToken(),
    profileInfo: {
      id: null,
      email: null,
      name: null
    },
  }),
  actions: {
    async profileData() {
      this.requestData.error = null;
      this.requestData.loading = true;
      try {
        const data = await apiProfileData();
        this.profileInfo.email = data.email;
        this.profileInfo.name = data.name;
        this.profileInfo.id = data.id;
      } catch (error) {
        this.requestData.error = error;
      }
      this.requestData.loading = false
    },
    async updateProfileData(email, name) {
      this.requestData.error = null;
      this.requestData.loading = true;
      try {
        const data = await apiUpdateProfile(email, name);
        this.profileInfo.email = data.email;
        this.profileInfo.name = data.name;
        this.profileInfo.id = data.id;
        this.requestData.loading = false;
        return true;
      } catch (error) {
        this.requestData.error = error;
      }
      this.requestData.loading = false;
      return false;
    },
    async login(email, password) {
      this.requestData.loading = true;
      this.requestData.error = null;

      try {
        const data = await apiLogin(email, password);
        this.token = data.token;
        storeToken(data.token);
      } catch (error) {
        this.requestData.error = error;
      }
      this.requestData.loading = false;
    },
    async register(email, password) {
      this.requestData.loading = true;
      this.requestData.error = null;
      try {
        const data = await apiRegister(email, password);
        storeToken(data.token);
      } catch (error) {
        this.requestData.error = error;
      }
      this.requestData.loading = false;
    },
    clearError() {
      this.requestData.error = null;
    },
  },
  getters: {
    isAuth(){
      return this.token !== null;
    }
  }
})

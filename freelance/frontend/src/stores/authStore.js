import {defineStore} from 'pinia'
import {apiRegistr, getProfile, login as apiLogin} from "@/services/api";
import {clearToken, getRefresh, getToken, storeToken} from "@/services/localData";
import {nextTick} from "vue";

export const useAuthStore = defineStore('authStore', {
    state: () => ({
        activeTab: true,
        access_token: getToken(),
        refresh_token: getRefresh(),
        isLoading: false,
        error: null,
        user: null,
        success: false,
        isDark: false,
    }),
    getters: {
        isAuth() {
            return this.user !== null;
        }
    },
    actions: {
        setFalse() {
            this.activeTab = false
        },
        setTrue() {
            this.activeTab = true
        },
        async register(email, password) {
            this.error = null
            try {
                const response = await apiRegistr(email, password);
                    if (response === 201) {
                        this.success = true
                    } else {
                        console.error ('Ошибка при регистрации')
                    }
            } catch (e) {
                this.error = e;

            }
        },
        async login(email, password) {
            this.isLoading = true;
            this.error = null;
            try {
                const tokens = await apiLogin(email, password);
                storeToken(tokens.access_token, tokens.refresh_token)
                this.access_token = tokens.access_token
                this.refresh_token = tokens.refresh_token
                await this.load();
                await nextTick()
            } catch (e) {
                this.error = e.message;
            }
            this.isLoading = false;
        },
        async load() {
            this.isLoading = true;
            try {
                this.user = await getProfile();
            } catch (e) {
                console.error(e);
            }
            this.isLoading = false;
        },
        async logout() {
            const response = await clearToken();
            console.log(response)
        },
        async toggle() {
          this.isDark = !this.isDark
        },

    },
})

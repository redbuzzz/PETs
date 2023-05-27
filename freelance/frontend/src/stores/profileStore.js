import {defineStore} from "pinia";
import {checkProfile, createprofile, getProfileFunction, updateEmail, updateProfileData} from "@/services/api";

export const useProfileStore = defineStore('profileStore', {
    state: () => ({
        isProfile: null,
        profileInfo: null,
        success: null,
        error: null,
        msg_error: 'Вы ввели неправильные данные',
        msg_success: 'Вы успешно обновили профиль',
    }),
    getters: {
        isHasProfile() {
            return this.isProfile === true;
        }
    },
    actions: {
        async checkProfile() {
            try {
                const response = await checkProfile();
                if (response === 200) {
                    this.profileInfo = await getProfileFunction();
                }
                if (response === 200) {
                    this.isProfile = true
                } else if (response === 404) {
                    this.isProfile = false
                }
            } catch (error) {
                console.log(error.message)
            }
        },
        async updateProfileWithoutEmail(last_name, first_name, birth_date, location) {
            this.success = null
            this.error = null
            try {
                const response = await updateProfileData(last_name, first_name, birth_date, location)
                if (response === 200) {
                    this.success = this.msg_success
                    setTimeout(() => {
                        this.success = null;
                    }, 10000);
                }
            } catch (error) {
                this.error = this.msg_error
                setTimeout(() => {
                    this.error = null;
                }, 10000);
                console.log(error.message)
            }
        },
        async updateProfileEmail(email, password) {
            this.success = null
            this.error = null
            try {
                const response = await updateEmail(email, password);
                console.log(response)
                if (response === 204) {
                    this.success = this.msg_success
                    setTimeout(() => {
                        this.success = null;
                    }, 10000);
                }
            } catch (error) {
                this.error = this.msg_error
                setTimeout(() => {
                    this.error = null;
                }, 10000);
                console.log(error.message)
            }
        },
        async createProfile() {
            try {
                const response = await createprofile();
                if (response) {
                    this.isProfile = true;
                }
            } catch (error) {
                console.error(error.message)
            }
        },

    },
})


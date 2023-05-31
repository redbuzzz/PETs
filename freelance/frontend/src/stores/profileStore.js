import {defineStore} from "pinia";
import {
    checkProfile, chooseCustomer, chooseFreelancer,
    createCustomer, createFreelancer,
    createprofile,
    getProfileFunction,
    updateEmail,
    updateProfileData
} from "@/services/api";

export const useProfileStore = defineStore('profileStore', {
    state: () => ({
        isProfile: null,
        profileInfo: null,
        success: null,
        isSuccess: null,
        error: null,
        isError: null,
        msg_error: 'Вы ввели неправильные данные',
        msg_success: 'Вы успешно обновили профиль',
        isCustomer: null,
        isFreelancer: null,
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
        async chooseCustomerRole() {
            try {
                await chooseCustomer();
                this.isCustomer = true;
                this.isFreelancer = false;
            } catch (error) {
                console.error(error.message)
            }
        },
        async chooseFreelancerRole() {
            try {
                await chooseFreelancer();
                this.isCustomer = false;
                this.isFreelancer = true;
            } catch (error) {
                console.error(error.message)
            }
        },
        async updateProfileWithoutEmail(last_name, first_name, birth_date, location) {
            this.isSuccess = null
            this.isError = null
            try {
                const response = await updateProfileData(last_name, first_name, birth_date, location)
                if (response === 200) {
                    this.isSuccess = this.msg_success
                    setTimeout(() => {
                        this.isSuccess = null;
                    }, 10000);
                }
            } catch (error) {
                this.isError = this.msg_error
                setTimeout(() => {
                    this.isError = null;
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
                    await createCustomer();
                    await createFreelancer();
                }
            } catch (error) {
                console.error(error.message)
            }
        },

    },
})


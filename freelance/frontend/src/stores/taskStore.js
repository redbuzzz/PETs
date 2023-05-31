import {defineStore} from "pinia";
import {getTasks} from "@/services/api";

export const useTaskStore = defineStore('taskStore', {
    state: () => ({
        isLoading: false,
        error: null,
        results: [],
        params: {
            search: null,
            category_id: null
        }
    }),
    actions: {
        async load() {
            this.isLoading = true;
            this.error = null;
            try {
                const params = {
                    ...this.params,
                    title: this.params.search
                }
                const responseData = await getTasks(params);
                this.params = params
                this.results = responseData;
            } catch (e) {
                this.error = e.message;
            }
            this.isLoading = false;
        },
        setParameter(key, value) {
            this.params[key] = value;
        },
        setParameters(params) {
            this.params = params;
        },

    }
})
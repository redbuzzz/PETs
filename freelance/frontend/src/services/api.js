import axios from 'axios';
import {API_URL} from "../../consts";
import router from "@/router";
import {useAuthStore} from "@/stores/authStore";
import {setAccess} from "@/services/localData";


const api = axios.create({
    baseURL: API_URL,
});

api.interceptors.request.use(function (config) {
    const auth = useAuthStore();
    if (auth.access_token) {
        config.headers['Authorization'] = `JWT ${auth.access_token}`;
    }
    return config;
}, function (error) {
    return Promise.reject(error);
});


api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const auth = useAuthStore();
        if (error.response && error.response.status === 401) {
            try {
                const response = await axios.post(`${API_URL}/auth/jwt/refresh/`, {
                    refresh: auth.refresh_token
                });
                const {access} = response.data;
                const {config} = error;
                config.headers['Authorization'] = `JWT ${access}`;
                setAccess(access)
                return axios.request(config);
            } catch (error) {
                console.error('Не удалось авторизоваться', error);
                await router.push({name: 'login'});
            }
        }
        return Promise.reject(error);
    },
);


export async function login(email, password) {
    try {
        const response = await axios.post(`${API_URL}/auth/jwt/create/`, {email, password});
        return {
            access_token: response.data.access,
            refresh_token: response.data.refresh,
        };
    } catch (error) {
        if (error.response && [400, 401].includes(error.response.status)) {
            throw new Error('Не удалось авторизоваться');
        } else {
            console.error('Произошла неизвестная ошибка', error);
            throw new Error('Произошла неизвестная ошибка, попробуйте еще раз');
        }
    }
}

export async function apiRegistr(email, password) {
    try {
        const response = await axios.post(`${API_URL}/auth/users/`, {email, password});
        return response.status
    } catch (error) {
        if (error.response && [400, 401].includes(error.response.status)) {
            if (error.response.data.email) {
                console.error(error.response.data);
                throw 'Такой пользователь уже существует';
            } else if (error.response.data.password) {
                const passwordErrors = error.response.data.password.map((errorMsg) => {
                    switch (errorMsg) {
                        case 'This password is too short. It must contain at least 8 characters.':
                            return 'Пароль слишком короткий. Он должен содержать не менее 8 символов.';
                        case 'This password is too common.':
                            return 'Пароль слишком простой.';
                        case 'This password is entirely numeric.':
                            return 'Пароль должен содержать не только цифры.';
                        default:
                            return errorMsg;
                    }
                });
                throw passwordErrors.join(', ');
            } else {
                console.error('Произошла неизвестная ошибка', error);
                throw new Error('Произошла неизвестная ошибка, попробуйте еще раз');
            }
        }
    }
}


export async function getProfile() {
    const response = await api.get('/is_auth/');
    return response.data;
}

export async function getTasks(params) {
    const response = await api.get("/tasks/", {params});
    return response.data;
}

export async function getCategory() {
    const response = await api.get("/category/");
    return response.data;
}

export async function createprofile() {
    const response = await api.post("/profile/");
    return response.data;
}

export async function checkProfile() {
    const response = await api.get("/profile_check/");
    return response.status
}


export async function getProfileFunction() {
    const response = await api.get("/profile/");
    return response.data;
}

export async function updateEmail(email, password) {
    const response = await api.post('/auth/users/set_email/', {
        new_email: email,
        current_password: password
    });
    console.log(response);
    return response.status;
}

export async function updateProfileData(last_name, first_name, birth_date, location) {
    const response = await api.patch('/profile/',
        {last_name, first_name, birth_date, location});
    return response.status

}

export default api;

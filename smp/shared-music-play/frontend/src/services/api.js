import {API_URL} from "./consts";
import axios from "axios";
import {useUserStore} from "@/stores/UserStore";

const instance = axios.create({
    baseURL: API_URL,
});

const noAuthInstance = axios.create({
  baseURL: API_URL
})

instance.interceptors.request.use(function (config) {
    const userStore = useUserStore();
    if (userStore.getToken()) {
        config.headers['Authorization'] = `Token ${userStore.getToken()}`;
    }
    return config;
}, function (error) {
    return Promise.reject(error);
});

noAuthInstance.interceptors.request.use(config => config, function (error) {
  return Promise.reject(error)
})

export async function apiLogin(email, password) {
  const response = await noAuthInstance.post('/login', {
    user: {
      email,
      password
    }
  }).catch(apiErrorHandler)

  return response.data;
}

export async function apiRegister(email, password) {
  const response = await noAuthInstance.post('/registr', {
    user: {
      email,
      password
    }
  }).catch(apiErrorHandler)

  return response.data;
}

export async function apiFetchRooms() {
  const response = await instance.get('/rooms/brief')
    .catch(apiErrorHandler)

  return response.data;
}

export async function apiFetchActiveRoom(id) {
  const response = await instance.get(`/rooms/${id}`)
    .catch(apiErrorHandler)

  return response.data;
}

export async function apiJoinRoom(code) {
  const response = await instance.post("/rooms/join/", {
    code
  }).catch(apiErrorHandler);

  return response.data;
}

export async function apiCreateRoom(name, privacy) {
  const response = await instance.post("/rooms/", {
    name, privacy
  }).catch(apiErrorHandler);

  return response.data;
}

export async function apiSavePlaylist(id, playlistIds) {
  const response = await instance.put(`/rooms/${id}/playlist/order/`, {
    playlist: playlistIds
  }).catch(apiErrorHandler);

  return response.data;
}

function apiErrorHandler(error) {
  if (error.response) {
    console.error(error.response);
    let err = new Error(error.response.data.detail || "Unknown error");
    err.statusCode = error.response.status;
    throw err;
  } else {
    console.error('Unknown error: ', error.message);
    throw new Error("Unknown error, please try again");
  }
}

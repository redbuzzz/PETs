import {API_URL} from "./consts";
import axios from "axios";
import {useUserStore} from "@/stores/UserStore";
import {getToken} from "@/services/localData";

const instance = axios.create({
    baseURL: API_URL,
});

const noAuthInstance = axios.create({
  baseURL: API_URL
})

instance.interceptors.request.use(function (config) {
    const userStore = useUserStore();
    if (getToken()) {
        config.headers['Authorization'] = `Token ${getToken()}`;
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

export async function apiRegister(name, email, password) {
  const response = await noAuthInstance.post('/registr', {
    user: {
      name,
      email,
      password
    }
  }).catch(apiErrorHandler)

  return response.data;
}

export async function apiFetchRooms(limit, offset) {
  const response = await instance.get('/rooms/', {
    params: {limit, offset}
  })
    .catch(apiErrorHandler)

  return response.data;
}

export async function apiFetchPublicRooms(limit, offset) {
  const response = await instance.get('/rooms/public/', {
    params: {limit, offset}
  })
    .catch(apiErrorHandler)

  return response.data;
}

export async function apiFetchActiveRoom(id) {
  const response = await instance.get(`/rooms/${id}`)
    .catch(apiErrorHandler)

  return response.data;
}

export async function apiFetchActiveRoomBans(id) {
  const response = await instance.get(`/rooms/${id}/banned_users`)
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
    err.data = error.response.data;
    throw err;
  } else {
    console.error('Unknown error: ', error.message);
    throw new Error("Unknown error, please try again");
  }
}

export async function apiSearchVideo(query) {
  const response = await instance.get(`/search?search_text=${query}`)
    .catch(apiErrorHandler);

  return response.data;
}

export async function apiFetchRoomUsers(roomId) {
  const response = await instance.get(`/rooms/${roomId}/users/`)
    .catch(apiErrorHandler);

  return response.data;
}

export async function apiUpdateRoomRole(roomId, userId, data) {
  const response = await instance.patch(`/rooms/${roomId}/users/${userId}/role/`, data)
    .catch(apiErrorHandler);
  console.log(response.data)

  return response.data;
}

export async function apiProfileData() {
  const response = await instance.get(`/profile`).
  catch(apiErrorHandler);

  return response.data;
}

export async function apiUpdateProfile(email, name) {
  const response = await instance.put(`/profile`, {email, name}).
  catch(apiErrorHandler);

  return response.data;
}


export function storeToken(access_token, refresh_token) {
    localStorage.setItem("access_token", access_token);
    localStorage.setItem("refresh_token", refresh_token);
}

export function getToken() {
    return localStorage.getItem("access_token");
}

export function getRefresh() {
    return localStorage.getItem("refresh_token");
}

export function clearToken() {
    localStorage.setItem('access_token', null);
    localStorage.setItem('refresh_token', null);
}

export function setAccess(access) {
    localStorage.setItem('access_token', access)
}

export function storeToken(token) {
    localStorage.setItem("token", token);
}
export function getToken() {
    const token = localStorage.getItem("token");
    return token === "null" ? null : token
}

export function clearTokens() {
    localStorage.setItem("token", null);
}

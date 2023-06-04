// not just and array of ["public", "private"], because in future we might want to distinguish
// values that the user sees and values that we send to the server (option.value and option.name)
export const ROOM_PRIVACY_OPTIONS = [
    {
        value: "public"
    },
    {
        value: "private"
    }
];
export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export const ROOM_ROLES = [
  {
    label: "Administrator",
    value: "admin"
  },
  {
    label: "Moderator",
    value: "moderator"
  },
  {
    label: "User",
    value: "user"
  }
]

export const WEBSOCKET_URL = import.meta.env.VITE_WEBSOCKET_URL || API_URL
    .replace('http', 'ws')
    .replace('api', 'ws');

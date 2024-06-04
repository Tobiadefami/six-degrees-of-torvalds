import axios from "axios";

const api = axios.create({
  baseURL: "http://" + process.env.BACKEND_HOST,
  withCredentials: true,
});

export default api;

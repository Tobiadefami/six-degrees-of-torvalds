import axios from "axios";
console.log(process.env.REACT_APP_BACKEND_HOST);
const api = axios.create({
  baseURL: "http://" + process.env.REACT_APP_BACKEND_HOST,
  withCredentials: true,
});

export default api;

import axios from "axios";
import authHeader from "./auth-header";

const API_URL = process.env.REACT_APP_SERVER_URL;

const getUserInfo = () => {
  return axios.get(`${API_URL}/user`, { headers: authHeader() });
};

export default {
  getUserInfo,
};
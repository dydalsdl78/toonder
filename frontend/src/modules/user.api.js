import axios from "axios";
import authHeader from "./auth-header";

const API_URL = "http://localhost:8080/";

const getUserInfo = () => {
  return axios.get(API_URL + "user", { headers: authHeader() });
};

export default {
  getUserInfo,
};
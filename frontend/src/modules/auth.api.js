import axios from "axios";
import authHeader from "./auth-header";

// for local test
const API_URL = "http://127.0.0.1:8000/accounts/";
// for release
// const API_URL = "";

const join = (username, email, password, passwordConfirmation) => {
  return axios.post(API_URL + "signup/", {
    username,
    email,
    password,
    passwordConfirmation,
  });
};

const login = (email, password) => {
  return axios
    .post(API_URL + "api-token-auth/", {
      email,
      password,
    })
    .then((response) => {
      console.log(response);
      if (response.data.token) {
        localStorage.setItem("user", JSON.stringify(response.data.token));
      }

      return response.data;
    });
};

const getuser = (token) => {
  return axios.get(API_URL + "get_userinfo/", {
    headers: {
      Authorization: `JWT ${token}`,
    },
  });
};

const logout = () => {
  localStorage.removeItem("user");
};

export default {
  join,
  login,
  getuser,
  logout,
};

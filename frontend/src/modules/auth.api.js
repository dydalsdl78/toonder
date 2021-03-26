import axios from "axios";

// for local test
const API_URL = "http://localhost:8080/api/auth/";
// for release
// const API_URL = "";


const join = (username, email, password, passwordConfirm) => {
  return axios.post(API_URL + "signup", {
    username,
    email,
    password,
    passwordConfirm,
  });
};

const login = (email, password) => {
  return axios
    .post(API_URL + "signin", {
      email,
      password,
    })
    .then((response) => {
      if (response.data.accessToken) {
        localStorage.setItem("user", JSON.stringify(response.data));
      }

      return response.data;
    });
};

const logout = () => {
  localStorage.removeItem("user");
};

export default {
  join,
  login,
  logout,
};
import axios from "axios";
import authHeader from "./auth-header";

// for local test
const API_URL = process.env.REACT_APP_SERVER_URL;
// for release
// const API_URL = "";

const join = (username, email, password, passwordConfirmation) => {
  return axios.post(`${API_URL}/accounts/signup/`, {
    username,
    email,
    password,
    passwordConfirmation,
  });
};

const login = (email, password) => {
  return axios
    .post(`${API_URL}/accounts/api-token-auth/`, {
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

const refresh = (token) => {
  return axios
    .post(`${API_URL}/accounts/api-token-refresh/`, {
      token,
    })
    .then((res) => {
      if (res.data.token) {
        localStorage.setItem("user", JSON.stringify(res.data.token));
      }
    })
    .catch((err) => {
      console.log(err);
    });
};
const getuser = (token) => {
  return axios.get(`${API_URL}/accounts/get_userinfo/`, {
    headers: {
      Authorization: `JWT ${token}`,
    },
  });
};

const logout = () => {
  localStorage.removeItem("user");
};

const recomm_overall = async () => {
  const token = JSON.parse(localStorage.getItem("user"));
  const config = {
    headers: {
      Authorization: `JWT ${token}`,
    },
  };
  console.log(config);
  const res = await axios.get(`${API_URL}/recommends/recomm_overall/`, config);
  console.log(res);
  return res;
};

export default {
  join,
  login,
  refresh,
  getuser,
  logout,
  recomm_overall,
};

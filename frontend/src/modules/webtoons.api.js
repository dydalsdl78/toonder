import axios from "axios";

// for local test
const API_URL = "http://127.0.0.1:8000/webtoons/";
// for release
// const API_URL = "";
const token = JSON.parse(localStorage.getItem("user"));

const config = {
  headers: {
    Authorization: `JWT ${token}`,
  },
};

const main = () => {
  return axios.get(API_URL + "main/");
};

const getDetail = async (webtoon_number) => {
  const token = JSON.parse(localStorage.getItem("user"));
  const config = {
    headers: {
      Authorization: `JWT ${token}`,
    },
  };
  console.log(config);
  try {
    const res = await axios.get(API_URL + "detail/" + {webtoon_number} + "/", config);
    console.log(res);
    return res;
  } catch (err) {
    console.log(err);
  }
};

export default {
  main,
  getDetail,
};

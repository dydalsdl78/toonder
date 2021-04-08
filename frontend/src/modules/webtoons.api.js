import axios from "axios";

// for local test
const API_URL = process.env.REACT_APP_SERVER_URL;
// for release
// const API_URL = "";
const token = JSON.parse(localStorage.getItem("user"));

const config = {
  headers: {
    Authorization: `JWT ${token}`,
  },
};

const main = () => {
  return axios.get(`${API_URL}/webtoons/main/`);
};

const getDetail = async (webtoon_number) => {
  try {
    const res = await axios.get(
      `${API_URL}/webtoons/detail/${webtoon_number}/`
    );
    return res;
  } catch (err) {
    console.log(err);
  }
};

export default {
  main,
  getDetail,
};

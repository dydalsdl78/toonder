import axios from "axios";


const API_URL = process.env.REACT_APP_SERVER_URL;

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

const exports = {
  main,
  getDetail,
};

export default exports;

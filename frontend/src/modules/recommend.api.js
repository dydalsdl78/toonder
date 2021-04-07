import axios from "axios";

// for local test
const API_URL = "http://127.0.0.1:8000/recommends/";
// for release
// const API_URL = "";

const getAllRecommend = () => {
  return axios.get(API_URL + "recomm_overall/");
};

const getGenreRecommend = () => {
  return axios.get(API_URL + "recomm_genre/");
};

const getArtistRecommend = () => {
  return axios.get(API_URL + "recomm_artist/");
};

const getSummaryRecommend = () => {
  return axios.get(API_URL + "recomm_summary/");
};

const getScoreRecommend = () => {
  return axios.get(API_URL + "recomm_score/");
};

const getMediaRecommend = () => {
  return axios.get(API_URL + "recomm_media/");
};

const getRandomRecommend = () => {
  return axios.get(API_URL + "recomm_random/");
};

const getOppositionRecommend = () => {
  return axios.get(API_URL + "recomm_opposition/");
};

const getLikes = async () => {
  const token = JSON.parse(localStorage.getItem("user"));
  const config = {
    headers: {
      Authorization: `JWT ${token}`,
    },
  };
  console.log(config);
  try {
    const res = await axios.get(API_URL + "like/", config);
    console.log(res)
    return res;
  } catch (err) {
    console.log(err);
  }
};

const getFavs = async () => {
  const token = JSON.parse(localStorage.getItem("user"));
  const config = {
    headers: {
      Authorization: `JWT ${token}`,
    },
  };
  console.log(config);
  try {
    const res = await axios.get(API_URL + "favorite/", config);
    console.log(res);
    return res;
  } catch (err) {
    console.log(err);
  }
};

const postFav = async (number) => {
  const token = JSON.parse(localStorage.getItem("user"));
  const config = {
    headers: {
      Authorization: `JWT ${token}`,
    },
  };
  console.log(config);
  try {
    const res = await axios.post(API_URL + `favorite/${number}/`, {key:'value'}, config);
    console.log(res);
    return res;
  } catch (err) {
    console.log(err);
  }
};

const postLike = async (number) => {
  const token = JSON.parse(localStorage.getItem("user"));
  const config = {
    headers: {
      Authorization: `JWT ${token}`,
    },
  };
  console.log(config);
  try {
    const res = await axios.post(API_URL + `like/${number}/`, {key:'value'}, config);
    console.log(res);
    return res;
  } catch (err) {
    console.log(err);
  }
};

export default {
  getAllRecommend,
  getGenreRecommend,
  getArtistRecommend,
  getSummaryRecommend,
  getScoreRecommend,
  getMediaRecommend,
  getRandomRecommend,
  getOppositionRecommend,
  getLikes,
  getFavs,
  postLike,
  postFav,
};

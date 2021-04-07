import axios from "axios";

// for local test
const API_URL = process.env.REACT_APP_SERVER_URL;
// for release
// const API_URL = "";

const getAllRecommend = () => {
  return axios.get(`${API_URL}/recommends/recomm_overall/`);
};

const getGenreRecommend = () => {
  return axios.get(`${API_URL}/recommends/recomm_genre/`);
};

const getArtistRecommend = () => {
  return axios.get(`${API_URL}/recommends/recomm_artist/`);
};

const getSummaryRecommend = () => {
  return axios.get(`${API_URL}/recommends/recomm_summary/`);
};

const getScoreRecommend = () => {
  return axios.get(`${API_URL}/recommends/recomm_score/`);
};

const getMediaRecommend = () => {
  return axios.get(`${API_URL}/recommends/recomm_media/`);
};

const getRandomRecommend = () => {
  return axios.get(`${API_URL}/recommends/recomm_random/`);
};

const getOppositionRecommend = () => {
  return axios.get(`${API_URL}/recommends/recomm_opposition/`);
};

const getLikes = async () => {
  const token = JSON.parse(localStorage.getItem("user"));
  if (token) {
    const config = {
      headers: {
        Authorization: `JWT ${token}`,
      },
    };
    console.log(config);
    console.log(API_URL);
    try {
      const res = await axios.get(`${API_URL}/recommends/like/`, config);
      console.log(res);
      return res;
    } catch (err) {
      console.log(err);
    }
  }
};

const getFavs = async () => {
  const token = JSON.parse(localStorage.getItem("user"));
  if (token) {
    const config = {
      headers: {
        Authorization: `JWT ${token}`,
      },
    };
    console.log(config);
    console.log(API_URL);
    try {
      const res = await axios.get(`${API_URL}/recommends/favorite/`, config);
      console.log(res);
      return res;
    } catch (err) {
      console.log(err);
    }
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
    const res = await axios.post(`${API_URL}/recommends/favorite/${number}/`, {key:'value'}, config);
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
    const res = await axios.post(`${API_URL}/recommends/like/${number}/`, {key:'value'}, config);
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

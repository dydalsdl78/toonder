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

const getLikes = () => {
  return axios.get(`${API_URL}/recommends/like/`);
};

const getFavs = () => {
  return axios.get(`${API_URL}/recommends/favorite/`);
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
};

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

const getLikes = () => {
  return axios.get(API_URL + "like/");
};

const getFavs = () => {
  return axios.get(API_URL + "favorite/");
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

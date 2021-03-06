import React, { useEffect, useState, useContext } from "react";
import styled from "styled-components";
import Rating from "@material-ui/lab/Rating";
import Box from "@material-ui/core/Box";
import FavoriteIcon from "@material-ui/icons/Favorite";
import BookmarkIcon from "@material-ui/icons/Bookmark";
import PlayCircleFilledIcon from "@material-ui/icons/PlayCircleFilled";
import Recommend from "../modules/recommend.api";
import Webtoons from "../modules/webtoons.api";
import Spinner from "../Components/Spinner";
import { makeStyles } from "@material-ui/core";
import { useLocation } from "react-router";
import { AuthContext } from "../Context/context";

import "./Detail.css";


const MainImage = styled.img`
  width: "100%";
  height: auto;
`;

const useStyles = makeStyles({
  mainImage: {
    width: "100%",
    marginTop: 10,
    marginBottom: 10,
  },
  likeIcon: {
    fontSize: "35px",
    marginRight: "30px",
    cursor: "pointer",
    // '&:hover': {
    //   color: "red",
    // },
  },
  favIcon: {
    fontSize: "40px",
    marginRight: "20px",
    cursor: "pointer",
    // '&:hover': {
    //   color: "#ffa500",
    // },
  },
});

function Detail() {
  const classes = useStyles();
  const location = useLocation();
  const authContext = useContext(AuthContext);
  const [webtoon, setWebtoon] = useState(null);
  const [likes, setLikes] = useState([]);
  const [favs, setFavs] = useState([]);
  const [isLike, setIsLike] = useState(null);
  const [isFav, setIsFav] = useState(null);

  const update = async () => {
    const response = await Webtoons.getDetail(location.state.number);
    if (response) {
      setWebtoon(response.data);
    } else {
      console.log("no response");
    }
    if (authContext.isLoggedIn) {
      const likelist = await Recommend.getLikes();
      setLikes(likelist.data);
      const favlist = await Recommend.getFavs();
      setFavs(favlist.data);
    }
  };

  useEffect(() => {
    async function fetchData() {
      const response = await Webtoons.getDetail(location.state.number);
      if (response) {
        setWebtoon(response.data);
      } else {
        console.log("no response");
      }
      if (authContext.isLoggedIn) {
        const likelist = await Recommend.getLikes();
        setLikes(likelist.data);
        const favlist = await Recommend.getFavs();
        setFavs(favlist.data);
      }
    }
    fetchData();
  }, [authContext.isLoggedIn, location.state.number]);

  useEffect(() => {
    setTimeout(1000);
    if (
      likes.filter((like) => like.webtoon_number === webtoon.webtoon_number)
        .length
    )
      setIsLike(true);
    else setIsLike(false);
    if (
      favs.filter((fav) => fav.webtoon_number === webtoon.webtoon_number).length
    )
      setIsFav(true);
    else setIsFav(false);
  }, [likes, favs, webtoon]);

  const likeClick = () => {
    Recommend.postLike(webtoon.webtoon_number);
    update();
  };

  const favClick = () => {
    Recommend.postFav(webtoon.webtoon_number);
    update();
  };

  const playClick = () => {
    window.open(webtoon.webtoon_link);
  };

  if (!webtoon)
    return (
      <div className="spinner">
        <Spinner />
      </div>
    );
  return (
    <div className="container detail-card">
      <MainImage className={classes.mainImage} src={webtoon.thumbnail_url} />
      <div className=" d-flex justify-content-between">
        <p>
          <b>
            {webtoon.webtoon_name} / {webtoon.webtoon_writer}
          </b>
        </p>
        <p>
          <b>
            {webtoon.webtoon_platform} / {webtoon.serialized_day}??????
          </b>
        </p>
      </div>
      <div className="d-flex justify-content-between">
        <p className="text-black-50 ml-2">{webtoon.genres_list}</p>
        <Box component="fieldset" mb={3} borderColor="transparent">
          <Rating name="read-only" value={webtoon.webtoon_score} readOnly />
        </Box>
      </div>
      <div></div>
      <div className="my-auto">
        <FavoriteIcon
          className={classes.likeIcon}
          onClick={likeClick}
          style={isLike ? { color: "red" } : { color: "black" }}
        />
        <BookmarkIcon
          className={classes.favIcon}
          onClick={favClick}
          style={isFav ? { color: "#ffa500" } : { color: "black" }}
        />
        <PlayCircleFilledIcon
          className={classes.favIcon}
          onClick={playClick}
          style={{ color: "black" }}
        />
      </div>
      <hr />
      <p>{webtoon.overview}</p>
    </div>
  );
}

export default Detail;

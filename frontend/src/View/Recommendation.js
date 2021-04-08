import React, { useState, useEffect, useContext } from "react";
import { Redirect } from "react-router-dom";
import { Title } from "../Lib";
import SwipeCard from "../Components/SwipeCard";
import Spinner from "../Components/Spinner";
import AuthService from "../modules/auth.api";
import { AuthContext } from "../Context/context";
import "./Recommendation.css";

function Recommendation() {
  const [recommendations, setRecommendations] = useState([]);
  const authContext = useContext(AuthContext);
  const [loading, setLoading] = useState(true);

  function shuffle(array) {
    var currentIndex = array.length,
      temporaryValue,
      randomIndex;

    // While there remain elements to shuffle...
    while (0 !== currentIndex) {
      // Pick a remaining element...
      randomIndex = Math.floor(Math.random() * currentIndex);
      currentIndex -= 1;

      // And swap it with the current element.
      temporaryValue = array[currentIndex];
      array[currentIndex] = array[randomIndex];
      array[randomIndex] = temporaryValue;
    }

    return array;
  }

  useEffect(async () => {
    const res = await AuthService.recomm_overall();
    let recomm = res.data;
    console.log(recomm);
    let recomm_list = [];
    recomm.forEach((recommReason) => {
      for (const [reason, webtoons] of Object.entries(recommReason)) {
        console.log(reason, webtoons);
        if (Object.keys(webtoons).length !== 0) {
          webtoons.forEach((webtoon) => {
            webtoon["reason"] = reason;
            recomm_list.push(webtoon);
          });
        }
      }
    });
    let random_list = shuffle(recomm_list);
    setLoading(false);
    setRecommendations(random_list);
  }, []);

  return authContext.isLoggedIn ? (
    loading ? (
      <div className="spinner">
        <Spinner />
        <p>좋아할만한 웹툰을 고르고 있어요!</p>
      </div>
    ) : (
      <>
        <div className="container">
          <SwipeCard recommendations={recommendations} />
          <div className="tutorial">
            <p>⬆ 보러가기 ⬇ 상세페이지 </p>
            <p>⬅ 패스~ ➡ 좋아요!</p>
          </div>
        </div>
      </>
    )
  ) : (
    <Redirect
      to={{
        pathname: "/login",
      }}
    />
  );
}

export default Recommendation;

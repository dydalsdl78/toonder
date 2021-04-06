import React, { useState, useEffect } from "react";
import { Title } from "../Lib";
import SwipeCard from "../Components/SwipeCard";
import AuthService from "../modules/auth.api";

function Recommendation() {
  const [recommendations, setRecommendations] = useState([]);

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
    setRecommendations(random_list);
  }, []);

  return (
    <div className="container">
      <Title>Recommendation</Title>
      <SwipeCard recommendations={recommendations} />
    </div>
  );
}

export default Recommendation;

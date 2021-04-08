import React from "react";
import TinderCard from "react-tinder-card";
import "./SwipeCard.css";
import Recommend from "../modules/recommend.api";
import { useHistory } from "react-router";

export default function SwipeCard({ recommendations }) {
  const history = useHistory();
  const onSwipe = async (direction, recommendation) => {
    console.log("You swiped: " + direction, recommendation.webtoon_number);
    if (direction === "right") {
      Recommend.postLike(recommendation.webtoon_number);
    } else if (direction === "left") {
      console.log("left");
    } else if (direction === "up") {
      goWatch(recommendation.webtoon_link);
    } else if (direction === "down") {
      console.log("down");
      const number = recommendation.webtoon_number;
      history.push({
        pathname: `/detail/${number}`,
        state: { number: number },
      });
    } else {
      console.log("error");
    }
  };

  const onCardLeftScreen = (myIdentifier) => {
    console.log(myIdentifier + " left the screen");
  };

  const goWatch = (url) => {
    window.open(url);
  };
  return (
    <div className="cardContainer">
      {recommendations.map((recommendation, index) => {
        return (
          <TinderCard
            className="swipe"
            key={index}
            onSwipe={(dir) => onSwipe(dir, recommendation)}
            onCardLeftScreen={() =>
              onCardLeftScreen(recommendation.webtoon_name)
            }
          >
            <p className="pcard">{recommendation.reason}</p>
            <div
              style={{
                backgroundImage: "url(" + recommendation.thumbnail_url + ")",
              }}
              className="card"
            >
              <h2>{recommendation.webtoon_score.toFixed(1)}</h2>
              <h3>{recommendation.webtoon_name}</h3>
              <h5>{recommendation.webtoon_writer}</h5>
            </div>
          </TinderCard>
        );
      })}
    </div>
  );
}

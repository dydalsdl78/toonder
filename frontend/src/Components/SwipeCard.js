import React from "react";
import TinderCard from "react-tinder-card";
import "./SwipeCard.css";
import Recommend from "../modules/recommend.api";

export default function SwipeCard({ recommendations }) {
  const onSwipe = async (direction, recommendation) => {
    console.log("You swiped: " + direction, recommendation.webtoon_number);
    if (direction == "right") {
      console.log("here");
      Recommend.postLike(recommendation.webtoon_number);
    } else if (direction == "left") {
      console.log("left");
    } else if (direction == "up") {
      goWatch(recommendation.webtoon_link);
    } else if (direction == "down") {
      console.log("down");
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
      {recommendations.map((recommendation) => {
        return (
          <TinderCard
            className="swipe"
            key={recommendation.webtoon_name}
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

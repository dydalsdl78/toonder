import React from "react";
import TinderCard from "react-tinder-card";
import "./SwipeCard.css";
import Recommend from "../modules/recommend.api";
import { useHistory } from "react-router";

export default function SwipeCard({ recommendations }) {
  const history = useHistory();

  const onSwipe = async (direction, recommendation) => {
    if (direction === "right") {
      Recommend.postLike(recommendation.webtoon_number);
    } else if (direction === "left") {
    } else if (direction === "up") {
      goWatch(recommendation.webtoon_link);
    } else if (direction === "down") {
      const number = recommendation.webtoon_number;
      history.push({
        pathname: `/detail/${number}`,
        state: { number: number },
      });
    } else {
      console.log("error");
    }
  };

  const onCardLeftScreen = (myIdentifier) => {};

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
            <div
              style={{
                backgroundImage: "url(" + recommendation.thumbnail_url + ")",
              }}
              className="card"
            >
              <h2>{recommendation.webtoon_score.toFixed(1)}</h2>
              <div className="card-description">
                <h3>{recommendation.webtoon_name}</h3>
                <br />
                <h3>{recommendation.webtoon_writer}</h3>
                <br />
                {"similar_webtoon" in recommendation ? (
                  <>
                    <p>
                      좋아하시는 작품 {recommendation.similar_webtoon}과(와)
                      비슷한 줄거리의 작품입니다
                    </p>
                  </>
                ) : (
                  <p>{recommendation.reason}</p>
                )}
              </div>
            </div>
          </TinderCard>
        );
      })}
    </div>
  );
}

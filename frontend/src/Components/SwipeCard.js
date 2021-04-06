import React from "react";
import TinderCard from "react-tinder-card";
import "./SwipeCard.css";

export default function SwipeCard() {
  const recommendations = [
    {
      name: "Richard Hendricks",
      url:
        "http://image.kmib.co.kr/online_image/2020/1209/611711110015305265_1.jpg",
    },
    {
      name: "Richard ",
      url:
        "http://image.kmib.co.kr/online_image/2020/1209/611711110015305265_1.jpg",
    },
    {
      name: "Richard fgsdf",
      url:
        "http://image.kmib.co.kr/online_image/2020/1209/611711110015305265_1.jpg",
    },
    {
      name: "Richard sdfwerewre",
      url:
        "http://image.kmib.co.kr/online_image/2020/1209/611711110015305265_1.jpg",
    },
    {
      name: "Richard Hendricks",
      url:
        "http://image.kmib.co.kr/online_image/2020/1209/611711110015305265_1.jpg",
    },
    {
      name: "Richard ",
      url:
        "http://image.kmib.co.kr/online_image/2020/1209/611711110015305265_1.jpg",
    },
    {
      name: "Richard fgsdf",
      url:
        "http://image.kmib.co.kr/online_image/2020/1209/611711110015305265_1.jpg",
    },
    {
      name: "Richard sdfwerewre",
      url:
        "http://image.kmib.co.kr/online_image/2020/1209/611711110015305265_1.jpg",
    },
  ];

  const onSwipe = (direction) => {
    console.log("You swiped: " + direction);
  };

  const onCardLeftScreen = (myIdentifier) => {
    console.log(myIdentifier + " left the screen");
  };

  return (
    <div className="cardContainer">
      {recommendations.map((recommendation) => {
        return (
          <TinderCard
            className="swipe"
            key={recommendation.name}
            onSwipe={(dir) => onSwipe(dir, recommendation.name)}
            onCardLeftScreen={() => onCardLeftScreen(recommendation.name)}
          >
            <div
              style={{ backgroundImage: "url(" + recommendation.url + ")" }}
              className="card"
            >
              <h3>{recommendation.name}</h3>
            </div>
          </TinderCard>
        );
      })}
    </div>
  );
}

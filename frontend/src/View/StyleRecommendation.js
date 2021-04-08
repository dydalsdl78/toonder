import React, { useState, useEffect } from "react";
import "./StyleRecommendation.css";
import Recommend from "../modules/recommend.api";
import Carousel from "react-multi-carousel";
import "react-multi-carousel/lib/styles.css";
import MediaCard from "../Components/MediaCard";

export default function StyleRecommendation() {
  const [webtoonList, setWebtoonList] = useState([]);

  useEffect(() => {
    async function fetchData() {
      const res = await Recommend.recommStyle();
      console.log(res.data);
      setWebtoonList(res.data);
    }
    fetchData();
  }, []);

  const responsive = {
    desktop: {
      breakpoint: { max: 3000, min: 1024 },
      items: 3,
      slidesToSlide: 3, // optional, default to 1.
    },
    tablet: {
      breakpoint: { max: 1024, min: 464 },
      items: 2,
      slidesToSlide: 2, // optional, default to 1.
    },
    mobile: {
      breakpoint: { max: 464, min: 0 },
      items: 1,
      slidesToSlide: 1, // optional, default to 1.
    },
  };

  const mainList = Object.entries(webtoonList).map(([genre, webtoons]) => {
    return (
      <div key={genre}>
        <h3 className="genre-title">{genre}</h3>
        <Carousel
          className="carousel"
          swipeable={true}
          draggable={true}
          showDots={true}
          responsive={responsive}
          ssr={true} // means to render carousel on server-side.
          infinite={true}
          keyBoardControl={true}
          customTransition="all .5"
          transitionDuration={500}
          containerClass="carousel-container"
          removeArrowOnDeviceType={["tablet", "mobile"]}
          dotListClass="custom-dot-list-style"
          itemClass="carousel-item-padding-40-px"
        >
          {webtoons.map((toon, index) => {
            return <MediaCard key={index} toon={toon} />;
          })}
        </Carousel>
      </div>
    );
  });

  return (
    <div className="container">
      <div className="main">
        <div className="main-image"></div>
        <div className="main-decription">
          <p>좋아하는 웹툰과 비슷한 작품을 찾아드리는 서비스입니다!</p>
          <p>
            그림체 분석 서비스는 현재 시범적으로 한가지 작품만 제공되고
            있습니다.
          </p>
          <p>이번에 선정된 작품은 학사재생입니다.</p>
        </div>
      </div>
      <br />

      <div className="style-recommendation">{mainList}</div>
    </div>
  );
}

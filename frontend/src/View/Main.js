import React, { useContext } from "react";
import Carousel from "react-multi-carousel";
import "react-multi-carousel/lib/styles.css";
import MediaCard from "../Components/MediaCard";
import { useHistory } from "react-router-dom";
import { AuthContext } from "../Context/context";
import "./Main.css";


function Main({ mainlist }) {
  const authContext = useContext(AuthContext);
  const history = useHistory();
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

  const handleClick = () => {
    history.push({
      pathname: `/style/`,
    });
  };

  const mainList = Object.entries(mainlist).map(([genre, webtoons]) => {
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
      <div>
        <p>{authContext.username}님 반갑습니다 ❤</p>
      </div>
      <div className="hero" onClick={handleClick}></div>
      <p className="hero-caption">
        툰더만의 그림체 추천 서비스를 확인해보세요!
      </p>
      <div>{mainList}</div>
    </div>
  );
}

export default Main;

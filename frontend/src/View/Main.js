import React, { useState } from "react";
import SearchBar from "../Components/SearchBar";
import { Title } from "../Lib";
import CarouselLine from "../Components/CarouselLine";

function Main() {
  const webtoons = [
    {
      공포: [
        {
          title: "으악",
          image:
            "http://image.kmib.co.kr/online_image/2020/1209/611711110015305265_1.jpg",
        },
        {
          title: "으악2",
          image:
            "http://image.kmib.co.kr/online_image/2020/1209/611711110015305265_1.jpg",
        },
        {
          title: "으악3",
          image:
            "http://image.kmib.co.kr/online_image/2020/1209/611711110015305265_1.jpg",
        },
        {
          title: "으악4",
          image:
            "http://image.kmib.co.kr/online_image/2020/1209/611711110015305265_1.jpg",
        },
        {
          title: "으악5",
          image:
            "http://image.kmib.co.kr/online_image/2020/1209/611711110015305265_1.jpg",
        },
      ],
      연애: [
        {
          title: "연애1",
          image:
            " http://www.econovill.com/news/photo/202004/393801_316518_230.jpg",
        },
        {
          title: "연애2",
          image:
            "http://www.econovill.com/news/photo/202004/393801_316518_230.jpg",
        },
      ],
      학교: [
        {
          title: "연애1",
          image:
            " http://www.econovill.com/news/photo/202004/393801_316518_230.jpg",
        },
        {
          title: "연애2",
          image:
            "http://www.econovill.com/news/photo/202004/393801_316518_230.jpg",
        },
      ],
    },
  ];

  return (
    <div className="container">
      <Title>Toonder</Title>
      {webtoons.map((webtoon) => (
        <CarouselLine webtoon={webtoon} />
      ))}
    </div>
  );
}

export default Main;

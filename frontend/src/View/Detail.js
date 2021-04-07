import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import { Title } from "../Lib";
import Rating from '@material-ui/lab/Rating';
import Box from '@material-ui/core/Box';
import Webtoons from '../modules/webtoons.api';

const MainImage = styled.img`
    width: '100%';
    height: auto;
`;

function Detail({ number }) {
  const [webtoon, setWebtoon] = useState(null);

  useEffect(async () => {
    const response = await Webtoons.getDetail(number);
    setWebtoon(response.data)
  }, [])
  console.log(webtoon)
  if (!webtoon) return <p>loading...</p> 
  return (
    <div className="container">
      <Title>상세페이지</Title>
      <MainImage src={webtoon.thumbnail_url}/>
      <p><b>{webtoon.webtoon_name} / {webtoon.webtoon_writer}</b></p>
      <p>{webtoon.overview}</p>
      <Box component="fieldset" mb={3} borderColor="transparent">
        <Rating name="read-only" value={webtoon.webtoon_score} readOnly />
      </Box>
    </div>
  );
}

export default Detail;
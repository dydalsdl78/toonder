import React, { useState } from "react";
import SearchBar from "../Components/SearchBar";
import Carousel from "../Components/Carousel";
import styled from 'styled-components';

const Title = styled.h1`
  color: #db5b33;
  font-weight: 300;
  text-align: center;
`;

function Main() {
  return (
    <>
      <SearchBar />
      <Title></Title>
      <Carousel images={images} />
    </>
  );
}

export default Main;

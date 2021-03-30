import React, { useState } from 'react';
import useCarousel from '../hooks/useCarousel';
import styled from 'styled-components';
import { makeStyles } from '@material-ui/core/styles';

const Container = styled.div`
  width: ${({ width }) => width}px;
  position: relative;
  margin: 0 auto;
  overflow: hidden;
  opacity: ${({ width }) => (width ? 1 : 0)}; ;
`;

const Slides = styled.div`
  display: flex;
  transition: transform ${({ duration }) => duration}ms ease-out;
  transform: translate3D(calc(var(--currentSlide) * -100%), 0, 0);
  transform: translate3D(${({ currentSlide }) => currentSlide * -100}%, 0, 0);
`;

const Img = styled.img`
  padding: 5px;
`;

const Control = styled.button`
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  font-size: 2em;
  color: #fff;
  background-color: transparent;
  border-color: transparent;
  cursor: pointer;
  z-index: 99;
  &:focus {
    outline: none;
  }
`;

const PrevControl = styled(Control)`
  left: 0;
`;

const NextControl = styled(Control)`
  right: 0;
`;

const Carousel = ({ images }) => {
  const { width, currentSlide, duration, isMoving, setWidth, setIsMoving, move } = useCarousel();

  const handleImageLoad = ({ target }) => {
    if (width !== target.offsetWidth) setWidth(target.offsetWidth);
    move(1);
  };

  const handleClick = ({ target: { id } }) => {
    if (isMoving) return;

    const delta = id === 'prev' ? -1 : 1;
    move(currentSlide + 1 * delta, 500);
  };

  const handleTransitionEnd = () => {
    setIsMoving(false);

    const delta = currentSlide === 0 ? 1 : currentSlide === images.length + 1 ? -1 : 0;

    if (delta) move(currentSlide + images.length * delta);
  };

  return (
    <Container width={width}>
      <Slides currentSlide={currentSlide} duration={duration} onTransitionEnd={handleTransitionEnd}>
        {[images[images.length - 1], ...images, images[0]].map((url, i) => (
          <Img key={i} src={url} onLoad={handleImageLoad} />
        ))}
      </Slides>
      <PrevControl id="prev" onClick={handleClick}>
        &laquo;
      </PrevControl>
      <NextControl id="next" onClick={handleClick}>
        &raquo;
      </NextControl>
    </Container>
  );
};

export default Carousel;
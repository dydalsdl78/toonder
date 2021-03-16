import React from "react";
import Navbar from "./Components/Navbar";
import { createGlobalStyle } from 'styled-components';

const GlobalStyle = createGlobalStyle`
  body{
    // background-color: black;
  };
`;

function App() {
  return (
    <div className="App">
      <GlobalStyle />
      <Navbar />
    </div>
  );
}

export default App;

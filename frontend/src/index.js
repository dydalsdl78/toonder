import React from "react";
import ReactDOM from "react-dom";
import App from "./App";
import { BrowserRouter as Router } from "react-router-dom";
import { createGlobalStyle } from "styled-components";

// import "bootstrap/dist/css/bootstrap.min.css";

const GlobalStyle = createGlobalStyle`
  body{
    // background-color: black;
  };
`;

ReactDOM.render(
  <React.StrictMode>
    <GlobalStyle />

    <Router>
      <App />
    </Router>
  </React.StrictMode>,
  document.getElementById("root")
);

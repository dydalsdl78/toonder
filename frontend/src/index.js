import React from "react";
import ReactDOM from "react-dom";
import App from "./App";
import { createStore, applyMiddleware } from 'redux';
import { Provider } from 'react-redux';
import ReduxThunk from 'redux-thunk';
import { BrowserRouter as Router} from "react-router-dom";
import { createGlobalStyle } from 'styled-components';
import rootReducer from './modules';

const store = createStore(rootReducer, applyMiddleware(ReduxThunk));

const GlobalStyle = createGlobalStyle`
  body{
    // background-color: black;
  };
`;

ReactDOM.render(
  <React.StrictMode>
    <GlobalStyle />
    <Router>
      <Provider store={store}>
        <App />
      </Provider>
    </Router>
  </React.StrictMode>,
  document.getElementById("root")
);

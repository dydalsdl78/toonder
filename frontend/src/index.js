import React from "react";
import ReactDOM from "react-dom";
import App from "./App";
import { createStore, applyMiddleware } from 'redux';
import { composeWithDevTools } from "redux-devtools-extension";
import { Provider } from 'react-redux';
import ReduxThunk from 'redux-thunk';
import { BrowserRouter as Router} from "react-router-dom";
import { createGlobalStyle } from 'styled-components';
import rootReducer from './reducers';

// import "bootstrap/dist/css/bootstrap.min.css";

const store = createStore(rootReducer, composeWithDevTools(applyMiddleware(ReduxThunk)));


const GlobalStyle = createGlobalStyle`
  body{
    // background-color: black;
  };
`;

ReactDOM.render(
  <React.StrictMode>
    <GlobalStyle />
    <Provider store={store}>
      <Router>
        <App />
      </Router>
    </Provider>
  </React.StrictMode>,
  document.getElementById("root")
);

import React from "react";
import { Switch, Redirect, Route } from "react-router-dom";
import Navbar from "./Components/Navbar";
import Login from "./View/Login";
import Join from "./View/Join";
import Main from "./View/Main";
import Recommendation from "./View/Recommendation";
import MyList from "./View/MyList";
import Profile from "./View/Profile";


function App() {
  let isAuthorized = false
  // let isAuthorized = localStorage.getItem("isAuthorized");

  return (
    <>
      {!isAuthorized ? <Redirect to="/login" /> : <Redirect to="/" />}
      <Switch>
        <Route>
          <Login path="/login" />
        </Route>
        <Route>
          <Login path="/join" />
        </Route>


        <Route exact path="/">
          <Main />
        </Route>
        <Route path="/recommendation">
          <Recommendation />
        </Route>
        <Route path="/mylist">
          <MyList />
        </Route>
        <Route path="/profile">
          <Profile />
        </Route>
      </Switch>
      <Navbar />
    </>
  );
}

export default App;

import React from "react";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
import Main from "../View/Main";
import Recommendation from "../View/Recommendation";
import MyList from "../View/MyList";
import Profile from "../View/Profile";

function Navbar() {
  return (
    <Router>
      <ul className="nav justify-content-around fixed-bottom mb-5">
        <li className="nav-item">
          <Link to="/">메인</Link>
        </li>
        <li className="nav-item">
          <Link to="/recommendation">추천만화</Link>
        </li>
        <li className="nav-item">
          <Link to="/mylist">내 리스트</Link>
        </li>
        <li className="nav-item">
          <Link to="/profile">프로필</Link>
        </li>
      </ul>

      <hr />

      <Switch>
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
    </Router>
  );
}

export default Navbar;

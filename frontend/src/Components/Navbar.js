import React from "react";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
import Main from "../View/Main";
import Recommendation from "../View/Recommendation";
import MyList from "../View/MyList";
import Profile from "../View/Profile";

function Navbar() {
  return (
    <Router>
      <div>
        <ul>
          <li>
            <Link to="/">메인</Link>
          </li>
          <li>
            <Link to="/recommendation">추천만화</Link>
          </li>
          <li>
            <Link to="/mylist">내 리스트</Link>
          </li>
          <li>
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
      </div>
    </Router>
  );
}

export default Navbar;

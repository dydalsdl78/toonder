import React from "react";
import { Switch, Route } from "react-router-dom";
import Navbar from "./Components/Navbar";
import Main from "./View/Main";
import Recommendation from "./View/Recommendation";
import MyList from "./View/MyList";
import Profile from "./View/Profile";




function App() {
  return (
    <div className="App">
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
      <Navbar />
    </div>
  );
}

export default App;

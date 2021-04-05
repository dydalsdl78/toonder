import React, { useSelector, useState, useEffect } from "react";
import {
  Switch,
  Redirect,
  Route,
  withRouter,
  useHistory,
} from "react-router-dom";
import Navbar from "./Components/Navbar";
import Login from "./View/Login";
import Join from "./View/Join";
import Main from "./View/Main";
import Recommendation from "./View/Recommendation";
import MyList from "./View/MyList";
import Profile from "./View/Profile";
import { AuthContext } from "./Context/context";
import AuthService from "./modules/auth.api";

function App() {
  const [token, setToken] = useState(null);
  const [username, setUsername] = useState(null);
  const [email, setEmail] = useState(null);

  const login = async (email, password) => {
    try {
      let res = await AuthService.login(email, password);
      setEmail(email);
      setToken(res.token);
      this.history.push("/");
    } catch (e) {
      console.log(e);
    }
  };

  const logout = () => {
    setToken(null);
    AuthService.logout();
  };

  useEffect(() => {
    const storedData = JSON.parse(localStorage.getItem("user"));
    if (storedData) {
      login(storedData);
    }
  }, [login]);

  const theme = {
    primary: "#00b8a9",
    secondary: "#f8f3d4",
    tertiary: "#f6416c",
    quaternary: "#ffde7d",
  };

  return (
    <>
      <AuthContext.Provider
        value={{
          isLoggedIn: !!token,
          login: login,
          logout: logout,
          username,
          setUsername,
          email,
          setEmail,
        }}
      >
        <Switch>
          <Route exact path="/">
            <Main />
          </Route>
          <Route path="/login">
            <Login />
          </Route>
          <Route path="/join">
            <Join />
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
      </AuthContext.Provider>
    </>
  );
}

export default App;

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
import Banner from "./Components/Banner";
import { AuthContext } from "./Context/context";
import AuthService from "./modules/auth.api";
import WebtoonService from "./modules/webtoons.api";

function App() {
  const [token, setToken] = useState(null);
  const [username, setUsername] = useState("guest");
  const [email, setEmail] = useState(null);
  const [mainlist, setMainlist] = useState([]);
  const [value, setValue] = useState("/");

  const login = async (email, password) => {
    try {
      let res = await AuthService.login(email, password);
      let userinfo = await AuthService.getuser(res.token);
      console.log("here", userinfo);
      setEmail(userinfo.data.email);
      setUsername(userinfo.data.username);
      setToken(res.token);
      this.history.push("/");
    } catch (e) {
      console.log(e);
    }
  };

  const getuser = async (token) => {
    try {
      const refresh = await AuthService.refresh(token);
      setToken(refresh);
      const userinfo = await AuthService.getuser(token);
      setEmail(userinfo.data.email);
      setUsername(userinfo.data.username);
    } catch (err) {
      console.log(err);
    }
  };

  const logout = () => {
    setToken(null);
    setEmail(null);
    setUsername("guest");
    AuthService.logout();
  };

  useEffect(async () => {
    const old_token = JSON.parse(localStorage.getItem("user"));
    const token = await AuthService.refresh(old_token);
    if (token) {
      try {
        getuser(token);
      } catch (err) {
        console.log(err);
        logout();
      }
    } else {
      console.log("로그인해주세요");
    }
  }, []);

  useEffect(async () => {
    const res = await WebtoonService.main();
    console.log(res.data);
    setMainlist(res.data);
  }, []);

  const theme = {
    primary: "#00b8a9",
    secondary: "#f8f3d4",
    tertiary: "#f6416c",
    quaternary: "#ffde7d",
  };

  return (
    <>
      <Banner />
      <AuthContext.Provider
        value={{
          isLoggedIn: !!token,
          login: login,
          logout: logout,
          username,
          setUsername,
          email,
          setEmail,
          getuser,
        }}
      >
        <Switch>
          <Route exact path="/">
            <Main mainlist={mainlist} />
          </Route>
          <Route path="/login">
            <Login value={value} setValue={setValue} />
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
        <Navbar value={value} setValue={setValue} />
      </AuthContext.Provider>
    </>
  );
}

export default App;

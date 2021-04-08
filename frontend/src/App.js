import React, { useState, useEffect } from "react";
import { Switch, Route, useHistory } from "react-router-dom";
import Navbar from "./Components/Navbar";
import Login from "./View/Login";
import Join from "./View/Join";
import Main from "./View/Main";
import Recommendation from "./View/Recommendation";
import MyList from "./View/MyList";
import Profile from "./View/Profile";
import Detail from "./View/Detail";
import Banner from "./Components/Banner";
import { AuthContext } from "./Context/context";
import AuthService from "./modules/auth.api";
import WebtoonService from "./modules/webtoons.api";

function App() {
  const history = useHistory();
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState("guest");
  const [email, setEmail] = useState(null);
  const [mainlist, setMainlist] = useState([]);
  const [value, setValue] = useState("/");

  const login = async (email, password) => {
    try {
      let res = await AuthService.login(email, password);
      let userinfo = await AuthService.getuser(res.token);
      setEmail(userinfo.data.email);
      setUsername(userinfo.data.username);
      setIsLoggedIn(true);
      setValue("/");
      history.push("/");
    } catch (e) {
      console.log(e);
      alert("회원정보가 틀렸습니다");
    }
  };

  const getuser = async (_token) => {
    try {
      const res = await AuthService.getuser(_token);
      setEmail(res.data.email);
      setUsername(res.data.username);
    } catch (err) {
      console.log(err);
    }
  };

  const logout = () => {
    setEmail(null);
    setUsername("guest");
    setIsLoggedIn(false);
    AuthService.logout();
  };

  useEffect(() => {
    async function fetchData() {
      const refresh = await AuthService.refresh(old_token);
      const userinfo = await AuthService.getuser(refresh);
      setEmail(userinfo.data.email);
      setUsername(userinfo.data.username);
      setIsLoggedIn(true);
    }
    const old_token = JSON.parse(localStorage.getItem("user"));
    if (old_token) {
      try {
        fetchData(old_token);
      } catch {
        console.log("logout");
        logout();
      }
    }
  }, []);

  useEffect(() => {
    async function fetchData() {
      const res = await WebtoonService.main();
      setMainlist(res.data);
    }
    fetchData();
  }, []);

  return (
    <>
      {/* {!isLoggedIn ? <Redirect to="/login" /> : <Redirect to="/" />} */}
      <Banner />
      <AuthContext.Provider
        value={{
          isLoggedIn,
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
          <Route path="/detail">
            <Detail />
          </Route>
        </Switch>
        <Navbar value={value} setValue={setValue} />
      </AuthContext.Provider>
    </>
  );
}

export default App;

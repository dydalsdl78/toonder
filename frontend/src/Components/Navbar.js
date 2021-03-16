import React from 'react';
import { BrowserRouter as Router, Switch, Route, useHistory } from "react-router-dom";
import { makeStyles } from '@material-ui/core/styles';
import BottomNavigation from '@material-ui/core/BottomNavigation';
import BottomNavigationAction from '@material-ui/core/BottomNavigationAction';
import HomeIcon from '@material-ui/icons/Home';
import ThumbUpIcon from '@material-ui/icons/ThumbUp';
import BookmarksIcon from '@material-ui/icons/Bookmarks';
import AccountBoxIcon from '@material-ui/icons/AccountBox';
import Main from "../View/Main";
import Recommendation from "../View/Recommendation";
import MyList from "../View/MyList";
import Profile from "../View/Profile";
// import styled from 'styled-components';



const useStyles = makeStyles({
  root: {
    width: "100%",
    backgroundColor: "#cee6b4",
    position: 'fixed',
    bottom: 0,
  },
});

function Navbar() {
  const history = useHistory();
  const classes = useStyles();
  const [value, setValue] = React.useState('/');

  const handleChange = (event, newValue) => {
    setValue(newValue);
    console.log(history);
    history.push({
      pathname: newValue,
    });
  };

  return (
    <Router>
      {/* <ul className="nav nav-pills nav-justified justify-content-around fixed-bottom bg-dark">
        <li className="nav-item">
          <Link to="/" className="nav-link active">메인</Link>
        </li>
        <li className="nav-item">
          <Link to="/recommendation" className="nav-link">추천만화</Link>
        </li>
        <li className="nav-item">
          <Link to="/mylist" className="nav-link">내 리스트</Link>
        </li>
        <li className="nav-item">
          <Link to="/profile" className="nav-link">프로필</Link>
        </li>
      </ul> */}
      <BottomNavigation value={value} onChange={handleChange} className={classes.root}>
        <BottomNavigationAction label="메인" value="/" icon={<HomeIcon/>}></BottomNavigationAction>
        <BottomNavigationAction label="추천만화" value="/recommendation" icon={<ThumbUpIcon/>}></BottomNavigationAction>
        <BottomNavigationAction label="내 리스트" value="/mylist" icon={<BookmarksIcon/>}></BottomNavigationAction>
        <BottomNavigationAction label="프로필" value="/profile" icon={<AccountBoxIcon/>}></BottomNavigationAction>
      </BottomNavigation>

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

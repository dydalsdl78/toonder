import React from "react";
import { withRouter, useHistory } from "react-router-dom";
import { makeStyles } from "@material-ui/core/styles";
import BottomNavigation from "@material-ui/core/BottomNavigation";
import BottomNavigationAction from "@material-ui/core/BottomNavigationAction";
import HomeIcon from "@material-ui/icons/Home";
import ThumbUpIcon from "@material-ui/icons/ThumbUp";
import BookmarksIcon from "@material-ui/icons/Bookmarks";
import AccountBoxIcon from "@material-ui/icons/AccountBox";
// import styled from 'styled-components';

const useStyles = makeStyles({
  root: {
    width: "100%",
    backgroundColor: "white",
    position: "fixed",
    bottom: 0,
  },
  selected: {
    color: "#f8f3d4",
  },
});

function Navbar({ value, setValue }) {
  const history = useHistory();
  const classes = useStyles();

  const handleChange = async (event, newValue) => {
    setValue(newValue);
    history.push(newValue);
  };

  return (
    <BottomNavigation
      value={value}
      onChange={handleChange}
      className={classes.root}
    >
      <BottomNavigationAction
        label="메인"
        value="/"
        icon={<HomeIcon />}
      ></BottomNavigationAction>
      <BottomNavigationAction
        label="추천만화"
        value="/recommendation"
        icon={<ThumbUpIcon />}
      ></BottomNavigationAction>
      <BottomNavigationAction
        label="내 리스트"
        value="/mylist"
        icon={<BookmarksIcon />}
      ></BottomNavigationAction>
      <BottomNavigationAction
        label="프로필"
        value="/profile"
        icon={<AccountBoxIcon />}
      ></BottomNavigationAction>
    </BottomNavigation>
  );
}

export default withRouter(Navbar);

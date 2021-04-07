import React, { useContext, useEffect } from "react";
import { Redirect, useHistory } from "react-router-dom";
import { AuthContext } from "../Context/context";
import { Title } from "../Lib";

import Avatar from "@material-ui/core/Avatar";
import Button from "@material-ui/core/Button";
import CssBaseline from "@material-ui/core/CssBaseline";
import TextField from "@material-ui/core/TextField";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Checkbox from "@material-ui/core/Checkbox";
import Link from "@material-ui/core/Link";
import Grid from "@material-ui/core/Grid";
import Box from "@material-ui/core/Box";
import FaceIcon from "@material-ui/icons/Face";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";
import Container from "@material-ui/core/Container";

import ProfileCard from "../Components/ProfileCard";

import AuthService from "../modules/auth.api";

const useStyles = makeStyles((theme) => ({
  paper: {
    marginTop: theme.spacing(8),
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    width: "100%", // Fix IE 11 issue.
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
}));

const Profile = () => {
  // if (!currentUser) {
  //   return <Redirect to="/login" />;
  // }
  const history = useHistory();
  const authContext = useContext(AuthContext);

  useEffect(async () => {
    const old_token = JSON.parse(localStorage.getItem("user"));
    const token = await AuthService.refresh(old_token);
    if (token) {
      try {
        authContext.getuser(token);
      } catch (err) {
        console.log(err);
      }
    }
  }, []);
  const classes = useStyles();

  return authContext.isLoggedIn ? (
    <Container component="main" maxWidth="xs">
      <CssBaseline />
      <div className={classes.paper}>
        <Avatar className={classes.avatar}>
          <FaceIcon />
        </Avatar>
        <Typography component="h1" variant="h5">
          {authContext.username}님의 프로필
        </Typography>
        <Grid container>
          <Grid xs={12}>sdfsadfsdfsdf</Grid>
          <Grid xs={9}>sdfasdfsdfsdf</Grid>
          <Grid xs={3}>sdfsdfsdfdsf</Grid>
          <Grid xs={3}>sdfsdfsdfdsf</Grid>
          <Grid xs={3}>sdfsdfsdfdsf</Grid>
          <Grid xs={3}>sdfsdfsdfdsf</Grid>
          <Grid xs={3}>sdfsdfsdfdsf</Grid>
          <Grid xs={3}>sdfsdfsdfdsf</Grid>
          <Grid xs={3}>sdfsdfsdfdsf</Grid>
          <Grid xs={3}>sdfsdfsdfdsf</Grid>
          <Grid xs={3}>sdfsdfsdfdsf</Grid>
        </Grid>
        <Button
          fullWidth
          variant="contained"
          color="primary"
          className={classes.submit}
          onClick={() => {
            history.push("/");
          }}
        >
          로그아웃 하기
        </Button>
      </div>
    </Container>
  ) : (
    <Redirect
      to={{
        pathname: "/login",
      }}
    />
  );
};

export default Profile;

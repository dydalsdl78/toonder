import React, { useState, useRef, useContext } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Redirect, withRouter, useHistory } from "react-router-dom";
import { useForm } from "react-hook-form";
// import Avatar from '@material-ui/core/Avatar';
// import LockOutlinedIcon from '@material-ui/icons/LockOutlined';

import Button from "@material-ui/core/Button";
import CssBaseline from "@material-ui/core/CssBaseline";
import TextField from "@material-ui/core/TextField";
// import FormControlLabel from '@material-ui/core/FormControlLabel';
// import Checkbox from '@material-ui/core/Checkbox';
import Link from "@material-ui/core/Link";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";
import Container from "@material-ui/core/Container";
import { AuthContext } from "../Context/context";
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
    width: "100%",
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
}));

function Login({ value, setValue }) {
  const authContext = useContext(AuthContext);
  const history = useHistory();
  const classes = useStyles();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  // const { message } = useSelector(state => state.message);

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("login");
    await authContext.login(email, password);
    setValue("/");
    history.push("/");
  };

  const onChangeEmail = (e) => {
    const email = e.target.value;
    setEmail(email);
  };

  const onChangePassword = (e) => {
    const password = e.target.value;
    setPassword(password);
  };
  if (AuthContext.username) {
    return <Redirect to="/" />;
  }

  return authContext.isLoggedIn ? (
    <Redirect
      to={{
        pathname: "/",
      }}
    />
  ) : (
    <Container component="main" maxWidth="xs">
      <CssBaseline />
      <div className={classes.paper}>
        {/* <Avatar className={classes.avatar}>
          <LockOutlinedIcon />
        </Avatar> */}
        <Typography component="h1" variant="h5">
          로그인해요
        </Typography>
        <form className={classes.form} onSubmit={handleSubmit}>
          <TextField
            variant="outlined"
            margin="normal"
            // required
            fullWidth
            id="email"
            label="이메일"
            name="email"
            value={email}
            onChange={onChangeEmail}
            autoComplete="email"
            autoFocus
          />
          <TextField
            variant="outlined"
            margin="normal"
            // required
            fullWidth
            name="password"
            value={password}
            onChange={onChangePassword}
            label="비밀번호"
            type="password"
            id="password"
            autoComplete="current-password"
          />
          {/* <FormControlLabel
            control={<Checkbox value="remember" color="primary" />}
            label="Remember me"
          /> */}
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            disabled={loading}
            className={classes.submit}
          >
            {loading ? "Loading" : "로그인"}
          </Button>
          <Grid container>
            <Grid item>
              <Link variant="body2" onClick={() => history.push("/join")}>
                {"처음 오셨나요? 회원가입!"}
              </Link>
            </Grid>
          </Grid>
        </form>
      </div>
    </Container>
  );
}
export default withRouter(Login);

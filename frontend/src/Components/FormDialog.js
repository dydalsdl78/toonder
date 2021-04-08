import React, { useState } from "react";
import Button from "@material-ui/core/Button";
import TextField from "@material-ui/core/TextField";
import Dialog from "@material-ui/core/Dialog";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogContentText from "@material-ui/core/DialogContentText";
import DialogTitle from "@material-ui/core/DialogTitle";
import { makeStyles } from "@material-ui/core/styles";
import { Redirect, useHistory } from "react-router-dom";
import AuthService from "../modules/auth.api";

export default function FormDialog() {
  const [open, setOpen] = React.useState(false);
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [passwordConfirmation, setPasswordConfirmation] = useState("");

  const onChangeCurrentPassword = (e) => {
    const password = e.target.value;
    setCurrentPassword(password);
  };
  const onChangeNewPassword = (e) => {
    const password = e.target.value;
    setNewPassword(password);
  };
  const onChangePasswordConfirmation = (e) => {
    const password = e.target.value;
    setPasswordConfirmation(password);
  };

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };
  const handleSubmit = async (e) => {
    const res = await AuthService.passwordChange(currentPassword, newPassword);
    alert(res.data);
    setOpen(false);
  };
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
      marginTop: "20px",
    },
  }));
  const classes = useStyles();
  return (
    <>
      <Button variant="outlined" color="primary" onClick={handleClickOpen}>
        변경
      </Button>
      <Dialog
        open={open}
        onClose={handleClose}
        aria-labelledby="form-dialog-title"
      >
        <DialogTitle id="form-dialog-title">비밀번호 확인</DialogTitle>
        <DialogContent>
          <DialogContentText>
            사용자 확인을 위하여 비밀번호를 입력해주시기 바랍니다.
          </DialogContentText>
          <form>
            <TextField
              autoFocus
              margin="dense"
              id="password"
              label="현재 비밀번호"
              type="password"
              value={currentPassword}
              onChange={onChangeCurrentPassword}
              fullWidth
            />
            <TextField
              autoFocus
              margin="dense"
              id="password"
              label="새로운 비밀번호"
              type="password"
              value={newPassword}
              onChange={onChangeNewPassword}
              fullWidth
            />
            <TextField
              autoFocus
              margin="dense"
              id="passwordConfirmation"
              label="비밀번호 확인"
              type="password"
              value={passwordConfirmation}
              onChange={onChangePasswordConfirmation}
              fullWidth
            />
          </form>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="primary">
            취소
          </Button>
          <Button onClick={handleSubmit} color="primary">
            회원정보 수정하기
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}

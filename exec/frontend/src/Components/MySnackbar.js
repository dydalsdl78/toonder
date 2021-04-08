import React from "react";
import Button from "@material-ui/core/Button";
import Snackbar from "@material-ui/core/Snackbar";


export default function MySnackbar() {
  const [state, setState] = React.useState(false);

  const handleClick = () => () => {
    setState(true);
    setInterval(handleClose(), 3000);
  };

  const handleClose = () => {
    setState(false);
  };

  const buttons = (
    <React.Fragment>
      dfdf
      <Button onClick={handleClick()}>Top-Center</Button>
    </React.Fragment>
  );

  return (
    <div>
      {buttons}
      <Snackbar open={state} onClose={handleClose} message="I love snacks" />
    </div>
  );
}

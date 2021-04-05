import React, { useContext } from "react";
import { Redirect } from "react-router-dom";
import { AuthContext } from "../Context/context";

const Profile = () => {
  // if (!currentUser) {
  //   return <Redirect to="/login" />;
  // }
  const authContext = useContext(AuthContext);

  return (
    <div className="container">
      <header className="jumbotron">
        <h3>
          <strong>이름</strong>
        </h3>
      </header>

      <p>
        <strong>Email:</strong>
        {authContext.email}
      </p>
    </div>
  );
};

export default Profile;

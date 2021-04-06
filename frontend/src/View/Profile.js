import React, { useContext } from "react";
import { Redirect } from "react-router-dom";
import { AuthContext } from "../Context/context";
import { Title } from "../Lib";

const Profile = () => {
  // if (!currentUser) {
  //   return <Redirect to="/login" />;
  // }
  const authContext = useContext(AuthContext);

  return (
    <div className="container">
      <Title>{authContext.username}'s Profile</Title>

      <p>
        <strong>Email:</strong>
        {authContext.email}
      </p>
    </div>
  );
};

export default Profile;

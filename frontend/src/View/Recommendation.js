import React, { useState, useEffect } from "react";
import { Title } from "../Lib";
import SwipeCard from "../Components/SwipeCard";
import AuthService from "../modules/auth.api";

function Recommendation() {
  const [recommendations, setRecommendations] = useState([]);

  useEffect(async () => {
    const res = await AuthService.recomm_overall();
    console.log(res.data);
    setRecommendations(res);
  }, []);

  return (
    <div className="container">
      <Title>Recommendation</Title>
      <SwipeCard recommendations={recommendations} />
    </div>
  );
}

export default Recommendation;

import React, { useState, useEffect } from 'react';
import { withRouter, useHistory } from "react-router-dom";
import { makeStyles } from '@material-ui/core/styles';
import SearchPreview from './SearchPreview';
// import styled from 'styled-components';



const useStyles = makeStyles({
});


function SearchBar() {
  const [keyword, setKeyword] = useState([]);
  const [searchKeyword, setSearchKeyword] = useState("");
  const [filteredPreview, setFilteredPreview] = useState([]);
  const history = useHistory();
  const classes = useStyles();

  const handleSearch = () => {
  };

  useEffect(() => {
    setFilteredPreview(() => {
      keyword.filter((pv) => pv.name.toLowerCase().includes(searchKeyword.toLowerCase()))
    }, [searchKeyword, keyword]);
  })

  return (
      <>
        <input
          type="search"
          placeholder="원하는 웹툰을 입력하세요."
          onChange={(e) => setSearchKeyword(e.target.value)}
        ></input>
        <SearchPreview preview={filteredPreview} />
      </>
  );
}

export default withRouter(SearchBar);
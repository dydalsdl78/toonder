import React, { useEffect, useState } from "react";
import { makeStyles } from "@material-ui/core/styles";
import Paper from "@material-ui/core/Paper";
import Tabs from "@material-ui/core/Tabs";
import Tab from "@material-ui/core/Tab";
import GridList from "@material-ui/core/GridList";
import GridListTile from "@material-ui/core/GridListTile";
import GridListTileBar from "@material-ui/core/GridListTileBar";
import FavoriteIcon from "@material-ui/icons/Favorite";
import BookmarkIcon from '@material-ui/icons/Bookmark';
import IconButton from '@material-ui/core/IconButton';
import Recommend from "../modules/recommend.api";
import { FavoriteSharp } from "@material-ui/icons";
import { useHistory } from "react-router";

const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
    flexWrap: "wrap", 
    justifyContent: "space-around",
    overflow: "hidden",
    backgroundColor: theme.palette.background.paper,
  },
  gridList: {
    width: "100%",
    height: "100%",
  },
  tabBar: {
    flexGrow: 1,
    width: "100%",
  },
  icon: {
    color: 'rgba(255, 255, 255, 0.54)',
  },
}));

function MyList() {
  const classes = useStyles();
  const history = useHistory();
  const [value, setValue] = useState(0);
  const [view, setView] = useState([]);
  const [likes, setLikes] = useState([]);
  const [favs, setFavs] = useState([]);
  const [mode, setMode] = useState('fav');

  const handleClick = (number) => {
    console.log(number)
    history.push({
      pathname: "/detail",
      state: {number:number}
    });
  };

  const update1 = async () => {
    const favlist = await Recommend.getFavs();
    setFavs(favlist.data);
    const likelist = await Recommend.getLikes();
    setLikes(likelist.data);
  };

  const update2 = async () => {
    const likelist = await Recommend.getLikes();
    setLikes(likelist.data);
    const favlist = await Recommend.getFavs();
    setFavs(favlist.data);
  };

  useEffect(async () => {
    const likelist = await Recommend.getLikes();
    setLikes(likelist.data);
    const favlist = await Recommend.getFavs();
    setFavs(favlist.data);
    setView(favlist.data);
  }, []);

  useEffect(()=>{
    setTimeout(1000)
    if (mode==="fav") setView(favs)
    if (mode==="like") setView(likes)
  },[likes,favs,view])

  const likeClick = (e, number) => {
    Recommend.postLike(number)
    update1();
    e.stopPropagation();
  }
  
  const favClick = (e, number) => {
    Recommend.postFav(number)
    update2();
    e.stopPropagation();
  }

  console.log("view : ", view);
  const handleChange = (e, newValue) => {
    setValue(newValue);
  };
  
  return (
    <>
      <Paper sqaure className={classes.tabBar}>
        <Tabs
          value={value}
          onChange={handleChange}
          variant="fullWidth"
          indicatorColor="secondary"
          textColor="secondary"
          aria-label="icon label tabs example"
        >
          <Tab
            icon={<BookmarkIcon />}
            label="Favorites"
            onClick={() => {
              setMode('fav')
              setView(favs);
            }}
            />
          <Tab
            icon={<FavoriteIcon />}
            label="Likes"
            onClick={() => {
              setMode('like')
              setView(likes);
            }}
          />
        </Tabs>
      </Paper>
      <div className={classes.root}>
        <GridList cellHeight={180} className={classes.gridList}>
          {view.map((li) => (
            <GridListTile key={li.webtoon_number} onClick={handleClick.bind(this, li.webtoon_number)}>
              <img src={li.thumbnail_url} alt={li.webtoon_name} />
              <GridListTileBar
                title={li.webtoon_name}
                subtitle={<span>{li.webtoon_writer}</span>}
                actionIcon={
                  mode==='like' ?
                  <IconButton aria-label={`info about ${li.webtoon_name}`} className={classes.icon}>
                    <FavoriteIcon onClick={(e) => likeClick(e, li.webtoon_number)} 
                    style={likes.filter((like)=>like.webtoon_number===li.webtoon_number).length ? {color:"red", opacity:0.54}: {color:'rgba(255, 255, 255, 0.54)'}}/>
                  </IconButton>
                  :
                  <IconButton aria-label={`info about ${li.webtoon_name}`} className={classes.icon}>
                    <BookmarkIcon onClick={(e) => favClick(e, li.webtoon_number)} 
                    style={favs.filter((fav)=>fav.webtoon_number===li.webtoon_number).length ? {color:"#ffa500", opacity:0.54}: {color:'rgba(255, 255, 255, 0.54)'}}/>
                  </IconButton>
                }
              />
            </GridListTile>
          ))}
        </GridList>
      </div>
    </>
  );
}

export default MyList;

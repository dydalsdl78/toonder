import React, { useEffect, useState, useContext } from "react";
import { Redirect } from "react-router-dom";
import { makeStyles } from "@material-ui/core/styles";
import Paper from "@material-ui/core/Paper";
import Tabs from "@material-ui/core/Tabs";
import Tab from "@material-ui/core/Tab";
import GridList from "@material-ui/core/GridList";
import GridListTile from "@material-ui/core/GridListTile";
import GridListTileBar from "@material-ui/core/GridListTileBar";
import FavoriteIcon from "@material-ui/icons/Favorite";
import BookmarkIcon from "@material-ui/icons/Bookmark";
import IconButton from "@material-ui/core/IconButton";
import Spinner from "../Components/Spinner";
import Recommend from "../modules/recommend.api";
import { useHistory } from "react-router";
import { AuthContext } from "../Context/context";

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
    color: "rgba(255, 255, 255, 0.54)",
  },
}));

function MyList() {
  const classes = useStyles();
  const history = useHistory();
  const authContext = useContext(AuthContext);
  const [loading, setLoading] = useState(true);
  const [value, setValue] = useState(0);
  const [view, setView] = useState([]);
  const [likes, setLikes] = useState([]);
  const [favs, setFavs] = useState([]);
  const [mode, setMode] = useState("like");

  useEffect(() => {
    if (authContext.isLoggedIn) {
      const fetchData = async () => {
        const likelist = await Recommend.getLikes();
        setLikes(likelist.data);
        const favlist = await Recommend.getFavs();
        setFavs(favlist.data);
        setView(likelist.data);
        setLoading(false);
      };
      fetchData();
    }
  }, [authContext, history]);

  const handleClick = (number) => {
    history.push({
      pathname: `/detail/${number}`,
      state: { number: number },
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

  const likeClick = (e, number) => {
    Recommend.postLike(number);
    update1();
    e.stopPropagation();
  };

  const favClick = (e, number) => {
    Recommend.postFav(number);
    update2();
    e.stopPropagation();
  };

  const handleChange = (e, newValue) => {
    setValue(newValue);
  };
  return authContext.isLoggedIn ? (
    loading ? (
      <div className="spinner">
        <Spinner />
        <p>좋아요 리스트 불러오는 중!</p>
      </div>
    ) : (
      <div className="container">
        <Paper sqaure="true" className={classes.tabBar}>
          <Tabs
            value={value}
            onChange={handleChange}
            variant="fullWidth"
            indicatorColor="secondary"
            textColor="secondary"
            aria-label="icon label tabs example"
          >
            <Tab
              icon={<FavoriteIcon />}
              label="Like"
              onClick={() => {
                setMode("like");
                setView(likes);
              }}
            />
            <Tab
              icon={<BookmarkIcon />}
              label="Favorites"
              onClick={() => {
                setMode("fav");
                setView(favs);
              }}
            />
          </Tabs>
        </Paper>
        <div className={classes.root}>
          <GridList cellHeight={180} className={classes.gridList}>
            {view.map((li) => (
              <GridListTile
                key={li.webtoon_number}
                onClick={handleClick.bind(this, li.webtoon_number)}
              >
                <img src={li.thumbnail_url} alt={li.webtoon_name} />
                <GridListTileBar
                  title={li.webtoon_name}
                  subtitle={<span>{li.webtoon_writer}</span>}
                  actionIcon={
                    mode === "like" ? (
                      <IconButton
                        aria-label={`info about ${li.webtoon_name}`}
                        className={classes.icon}
                        onClick={(e) => likeClick(e, li.webtoon_number)}
                      >
                        <FavoriteIcon
                          style={
                            likes.filter(
                              (like) =>
                                like.webtoon_number === li.webtoon_number
                            ).length
                              ? { color: "red", opacity: 0.54 }
                              : { color: "rgba(255, 255, 255, 0.54)" }
                          }
                        />
                      </IconButton>
                    ) : (
                      <IconButton
                        aria-label={`info about ${li.webtoon_name}`}
                        className={classes.icon}
                        onClick={(e) => favClick(e, li.webtoon_number)}
                      >
                        <BookmarkIcon
                          style={
                            favs.filter(
                              (fav) => fav.webtoon_number === li.webtoon_number
                            ).length
                              ? { color: "#ffa500", opacity: 0.54 }
                              : { color: "rgba(255, 255, 255, 0.54)" }
                          }
                        />
                      </IconButton>
                    )
                  }
                />
              </GridListTile>
            ))}
          </GridList>
        </div>
      </div>
    )
  ) : (
    <Redirect
      to={{
        pathname: "/login",
      }}
    />
  );
}

export default MyList;

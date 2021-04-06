import React, { useEffect, useState } from "react";
import { makeStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import GridList from '@material-ui/core/GridList';
import GridListTile from '@material-ui/core/GridListTile';
import GridListTileBar from '@material-ui/core/GridListTileBar';
import FavoriteIcon from '@material-ui/icons/Favorite';
import GradeIcon from '@material-ui/icons/Grade';
import Recommend from "../modules/recommend.api";

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'space-around',
    overflow: 'hidden',
    backgroundColor: theme.palette.background.paper,
  },
  gridList: {
    width: 500,
    height: 450,
  },
  tabBar: {
    flexGrow: 1,
    width: '100%',
  }
}));

function MyList() {
  const classes = useStyles();
  const [value, setValue] = useState(0);
  const [view, setView] = useState([]);
  const [likes, setLikes] = useState([]);
  const [favs, setFavs] = useState([]);

  useEffect(async () => {
    setLikes(await Recommend.getLikes())
    setFavs(await Recommend.getFavs())
    setView(favs)
  }, []);

  const handleChange = (e, newValue) => {
    setValue(newValue);
  };

  return (
    <div className={classes.root + ' container'}>
      <Paper sqaure className={classes.tabBar}>
        <Tabs
          value={value}
          onChange={handleChange}
          variant="fullWidth"
          indicatorColor="secondary"
          textColor="secondary"
          aria-label="icon label tabs example"
        >
          <Tab icon={<GradeIcon />} label="Favorites" onClick={() => {setView(favs)}}/>
          <Tab icon={<FavoriteIcon />} label="Likes" onClick={() => {setView(likes)}}/>
        </Tabs>
      </Paper>
      <GridList cellHeight={180} className={classes.gridList}>
        {view.map((li) => (
          <GridListTile key={li.webtoon_number}>
            <img src={li.thumbnail_url} alt={li.webtoon_name} />
            <GridListTileBar
              title={li.webtoon_name}
              subtitle={<span>{li.webtoon_writer}</span>}
            />
          </GridListTile>
        ))}
      </GridList>
    </div>
  );
}

export default MyList;

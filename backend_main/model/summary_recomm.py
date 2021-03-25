import json
import warnings
import numpy as np
import pandas as pd
from eunjeon import Mecab
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

warnings.filterwarnings('ignore')

def to_dataframe(data):
  
  ls_webtoon = []

  for i in range(len(data)):
    title = data[i].webtoon_name
    overview = data[i].overview
    artists = data[i].webtoon_writer
    image = data[i].thumbnail_url
    score = data[i].webtoon_score
    link = data[i].webtoon_link
    platform = data[i].webtoon_platform
    day = data[i].serialized_day

    ls_webtoon.append([title, overview, artists, image, score, link, platform, day)

  webtoon_df = pd.DataFrame(ls_webtoon, columns=['title', 'overview', 'artists', 'image', 'score', 'link', 'platform', 'day'])
  
  return webtoon_df

def tokenizer(webtoon_df):

  mecab = Mecab()
  webtoon_df['overview_token'] = webtoon_df['overview'].apply(lambda x: mecab.nouns(x))

  count_vect = TfidfVectorizer(min_df=0, ngram_range=(1, 2))
  genre_mat = count_vect.fit_transform(movies_df['overview_literal'])

  genre_sim = cosine_similarity(genre_mat, genre_mat)

  genre_sim_sorted_ind = genre_sim.argsort()[:, ::-1]

  return genre_sim_sorted_ind

def find_sim_movie_ver2(df, sorted_ind, title_name, top_n=10):
  title_movie = df[df['webtoon_name'] == title_name]
  title_index = title_movie.index.values

  similar_indexes = sorted_ind[title_index, :(top_n*2)]
  similar_indexes = similar_indexes.reshape(-1)

  similar_indexes = similar_indexes[similar_indexes != title_index]

  return df.iloc[similar_indexes][:top_n][['webtoon_name', 'overview', 'webtoon_writer', 'thumbnail_url', 'webtoon_score', 'webtoon_link', 'webtoon_platform', 'serialized_day']].to_json(orient='records', force_ascii=False)


def reults(title):
  similar_movies = find_sim_movie_ver2(webtoon_df, genre_sim_sorted_ind, '{}'.format(name), 10)
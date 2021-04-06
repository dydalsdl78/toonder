import json
import warnings
import numpy as np
import pandas as pd
from eunjeon import Mecab
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

warnings.filterwarnings('ignore')

# 데이터프레임화
def to_dataframe(data):
  
  ls_webtoon = []
  print("시작")
  for i in range(len(data)):
    num = data[i].webtoon_number
    title = data[i].webtoon_name
    # overview = data[i].overview
    # artists = data[i].webtoon_writer
    # image = data[i].thumbnail_url
    # score = data[i].webtoon_score
    # link = data[i].webtoon_link
    morphs = data[i].overview_morph
    # platform = data[i].webtoon_platform
    # day = data[i].serialized_day
    # genres = data[i].genres.all()
    # genres = [genre.id for genre in genres]

    # ls_webtoon.append([title, overview, artists, image, score, link, [morphs], platform, day, genres])
    ls_webtoon.append([num, title, [morphs]])

  webtoon_df = pd.DataFrame(ls_webtoon, columns=['webtoon_number', 'webtoon_name', 'overview_morph'])
  print("데이터프레임화")
  return webtoon_df

# 토큰화 및 tf-idf 행렬 계산
def tokenizer(webtoon_df):

  # mecab = Mecab()
  # webtoon_df['overview_token'] = webtoon_df['overview'].apply(lambda x: mecab.nouns(x))

  # print(webtoon_df['overview_token'][0])
  # print(webtoon_df['overview_morph'][0])

  webtoon_df['overview_literal'] = webtoon_df['overview_morph'].apply(lambda x: (' ').join(x))
  print(webtoon_df['overview_literal'])
  count_vect = TfidfVectorizer(min_df=0, ngram_range=(1, 2))
  token_mat = count_vect.fit_transform(webtoon_df['overview_literal'])

  token_sim = cosine_similarity(token_mat, token_mat)
  token_sim_sorted_ind = token_sim.argsort()[:, ::-1]
  print("토큰 및 행렬계산")
  # token_sim_sorted_val = np.sort(token_sim)[:, ::-1]
  # print(token_sim_sorted_val[30:50])
  return token_sim_sorted_ind

def opposition_tokenizer(webtoon_df):

  # mecab = Mecab()
  # webtoon_df['overview_token'] = webtoon_df['overview'].apply(lambda x: mecab.nouns(x))
  webtoon_df['overview_literal'] = webtoon_df['overview_morph'].apply(lambda x: (' ').join(x))
  count_vect = TfidfVectorizer(min_df=0, ngram_range=(1, 2))
  token_mat = count_vect.fit_transform(webtoon_df['overview_literal'])

  token_sim = cosine_similarity(token_mat, token_mat)
  token_sim_sorted_ind = token_sim.argsort()
  
  # token_sim_sorted_val = np.sort(token_sim)
  # print(token_sim_sorted_val[30:50])
  return token_sim_sorted_ind


# 유사도 계산
def find_sim_movie_ver2(df, sorted_ind, title_webtoon, top_n=10):
  title_webtoon = df[df['webtoon_name'] == title_webtoon]
  title_index = title_webtoon.index.values
  similar_indexes = sorted_ind[title_index, :(top_n*2)]
  similar_indexes = similar_indexes.reshape(-1)
  
  similar_indexes = similar_indexes[similar_indexes != title_index]
  print(similar_indexes)
  print("유사도계산")
  return df.iloc[similar_indexes][:top_n][['webtoon_number', 'webtoon_name']].to_json(orient='records', force_ascii=False)
  # return df.iloc[similar_indexes][:top_n][['webtoon_name', 'overview', 'webtoon_writer', 'thumbnail_url', 'webtoon_score', 'webtoon_link', 'webtoon_platform', 'serialized_day', "genres"]].to_json(orient='records', force_ascii=False)

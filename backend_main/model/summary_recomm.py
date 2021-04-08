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

  for i in range(len(data)):
    num = data[i].webtoon_number
    title = data[i].webtoon_name
    morphs = data[i].overview_morph
    
    ls_webtoon.append([num, title, [morphs]])

  webtoon_df = pd.DataFrame(ls_webtoon, columns=['webtoon_number', 'webtoon_name', 'overview_morph'])

  return webtoon_df

# 유사도 계산 후 높은 것 부터 정렬
def tokenizer(webtoon_df):

  webtoon_df['overview_literal'] = webtoon_df['overview_morph'].apply(lambda x: (' ').join(x))
  # 줄거리 TF-IDF 행렬을 벡터화
  count_vect = TfidfVectorizer(min_df=0, ngram_range=(1, 2))
  token_mat = count_vect.fit_transform(webtoon_df['overview_literal'])
  
  # 유사도 계산
  token_sim = cosine_similarity(token_mat, token_mat)
  token_sim_sorted_ind = token_sim.argsort()[:, ::-1]
  return token_sim_sorted_ind

# 유사도가 계산 후 낮은 것 부터 정렬
def opposition_tokenizer(webtoon_df):

  webtoon_df['overview_literal'] = webtoon_df['overview_morph'].apply(lambda x: (' ').join(x))
  count_vect = TfidfVectorizer(min_df=0, ngram_range=(1, 2))
  token_mat = count_vect.fit_transform(webtoon_df['overview_literal'])

  token_sim = cosine_similarity(token_mat, token_mat)
  token_sim_sorted_ind = token_sim.argsort()
  
  return token_sim_sorted_ind


# 유사도가 높거나 낮은 상위 10개 출력해서 응답 
def find_sim_movie_ver2(df, sorted_ind, title_webtoon, top_n=10):
  title_webtoon = df[df['webtoon_name'] == title_webtoon]
  title_index = title_webtoon.index.values
  similar_indexes = sorted_ind[title_index, :(top_n*2)]
  similar_indexes = similar_indexes.reshape(-1)
  
  similar_indexes = similar_indexes[similar_indexes != title_index]

  return df.iloc[similar_indexes][:top_n][['webtoon_number', 'webtoon_name']].to_json(orient='records', force_ascii=False)
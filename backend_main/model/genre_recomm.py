import json
import warnings
import numpy as np
import pandas as pd
from eunjeon import Mecab
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# from recommends.models import Webtoon

warnings.filterwarnings('ignore')

def to_dataframe(data):
  ls_webtoon = []

  # data = Webtoon.objects.all()

  for i in range(len(data)-5, len(data)):
    title = data[i].webtoon_name
    print(data[i].genres.all())
  # genres = 

  # ls_webtoon.append([title, overview, artists, image, score, link, platform, day])
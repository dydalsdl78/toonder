from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Webtoon
from .serializers import WebtoonSerializer, SummarySerializer
from model import summary_recomm
import json

def index(request):
    # webtoons = Webtoon.objects.all()

    # print(type(webtoons))
    # print(webtoons) # 전체 웹툰의 QuerySet
    # print(webtoons[1]) # 해당 웹툰의 QuerySet
    # print(webtoons[1].webtoon_name) # 해당 웹툰의 이름

    pass

# 전체 웹툰 리스트------------------------------------------------
@api_view(['GET'])
def webtoon_list(request):
    webtoons = Webtoon.objects.all()
    # 시리얼라이즈
    serializer = WebtoonSerializer(webtoons, many=True)
    return Response(serializer.data)


# 웹툰 추천 카드 관련---------------------------------------------
# 사용자 정보가 필요한 항목들--------------------------
def recomm_overall(request):
    pass
def recomm_genre(request):
    pass
def recomm_artist(request):
    pass

# 사용자 정보가 필요없는 항목들------------------------
@api_view(['POST'])
def recomm_summary(request):
    webtoons = Webtoon.objects.all()

    df_webtoon = summary_recomm.to_dataframe(webtoons)
    overview_sim_sorted_ind = summary_recomm.tokenizer(df_webtoon)
    title = request.data['title']
    # title = '학사재생'
    similar_webtoons = summary_recomm.find_sim_movie_ver2(df_webtoon, overview_sim_sorted_ind, '{}'.format(title), 10)
    results = json.loads(similar_webtoons)
    return Response(results)

@api_view(['GET'])
def recomm_score(request):
    webtoons = Webtoon.objects.order_by("-webtoon_score")[:10]
    # 시리얼라이즈
    serializer = WebtoonSerializer(webtoons, many=True)
    return Response(serializer.data)

def recomm_media(request):
    pass

@api_view(['GET'])
def recomm_random(request):
    webtoon = Webtoon.objects.order_by("?")[0]
    # 시리얼라이즈
    serializer = WebtoonSerializer(webtoon)
    return Response(serializer.data)
    
def recomm_opposition(request):
    # 어떤기준으로 완전 반대되는 추천??
    pass




# 유저 좋아요, 찜목록 리스트 관련----------------------------------

# 유저 좋아요 리스트 & 추가하기
def likes_list_create(request):
    # Webtoon.objects.create(request.data)
    pass

# 유저 좋아요 삭제하기
def likes_delete(request, pk):
    pass

# 유저 찜목록 리스트 & 추가하기
def favorite_list_create(request):
    pass

# 유저 찜목록 삭제하기
def favorite_delete(request, pk):
    pass


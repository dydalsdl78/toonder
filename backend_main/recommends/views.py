from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

from .serializers import WebtoonSerializer, GenreSerializer
from model import summary_recomm, genre_recomm
from .models import Webtoon, Genre

from drf_yasg import openapi
import json

# 장르별 웹툰 목록
class WebtoonMainViewSet(viewsets.ModelViewSet):
    """
        웹툰 메인 장르별 목록 출력
        ---
    """
    serializer_class = WebtoonSerializer

    def webtoon_main(self, request):
        genres = Genre.objects.all()
        webtoons = Webtoon.objects.all()
        for i in genres:
            print(i.id)
        result = {}
        for w in webtoons[:5]:
            serializer = GenreSerializer(w.genres, many=True)
            print(serializer.data)
        # for genre in genres[:5]:
        #     webtoon_genre_ls = []
        #     genre_name = genre.genre_name
        #     print(genre_name)
        #     for webtoon in webtoons:
        #         print(webtoon.webtoon_name)
        #         w_genres = webtoon.genres.all()
        #         for w_genre in w_genres:
        #             if genre_name == w_genre.genre_name and len(webtoon_genre_ls) < 9:
        #                 serializer = WebtoonSerializer(webtoon)
        #                 webtoon_genre_ls.append(serializer.data)
        #     result[genre_name] = webtoon_genre_ls
                
        return Response(0)    

# 전체 웹툰 리스트------------------------------------------------
class WebtoonListViewSet(viewsets.ModelViewSet):
    """
        웹툰 전체 목록 출력
        ---
    """
    serializer_class = WebtoonSerializer

    # @api_view(['GET'])
    def webtoon_list(self, request):
        webtoons = Webtoon.objects.all()
        serializer = WebtoonSerializer(webtoons, many=True)
        return Response(serializer.data)


# 사용자 정보가 필요한 항목들--------------------------
# 이건 뭐지?
def recomm_overall(request):
    pass


def recomm_genre(request):
    # 사용자의 장르 벡터
    webtoons = Webtoon.objects.all()
    df_webtoon = genre_recomm.to_dataframe(webtoons)
    
    # 웹툰들의 장르 벡터
    return Response(df_webtoon)


class WebtoonArtistViewSet(viewsets.ModelViewSet):
    """
        웹툰 작가 기반 추천
        ---
    """
    serializer_class = WebtoonSerializer

    @authentication_classes([JSONWebTokenAuthentication])
    @permission_classes([IsAuthenticated])    
    def recomm_artist(self, request):
        user_id = get_user_model().objects.values('user_id').filter(username="tester")
        # user_id = get_user_model().objects.values('user_id').filter(username=request.user)
        favorite_webtoons = Webtoon.objects.filter(users_webtoon=user_id[0]['user_id'])
        
        recommend_result = {}
        webtoons = Webtoon.objects.all()

        for favorite_webtoon in favorite_webtoons:
            writer = favorite_webtoon.webtoon_writer
            
            tmp = []

            for webtoon in webtoons:
                if webtoon.webtoon_writer in writer:
                    serializer = WebtoonSerializer(webtoon)
                    tmp.append(serializer.data)
                    recommend_result[writer] = tmp
        # 로그인된 사용자의 정보를 통해 찜목록에 있는 것을 갖고온다.
        # favorite_webtoons = Webtoon.objects.filter(webtoon_writer='찜목록의 작가이름')
        return Response(recommend_result)

# 사용자 정보가 필요없는 항목들------------------------
class WebtoonSummaryViewSet(viewsets.ModelViewSet):
    """
        웹툰 줄거리 기반 추천
        ---
    """
    serializer_class = WebtoonSerializer

    @authentication_classes([JSONWebTokenAuthentication])
    @permission_classes([IsAuthenticated]) 
    def recomm_summary(self, request):
        # 로그인 유저의 찜리스트 목록 가져오기
        user_id = get_user_model().objects.values('user_id').filter(username="tester")
        # user_id = get_user_model().objects.values('user_id').filter(username=request.user)
        favorite_webtoons = Webtoon.objects.filter(users_webtoon=user_id[0]['user_id'])
        
        webtoons = Webtoon.objects.all()

        df_webtoon = summary_recomm.to_dataframe(webtoons)
        overview_sim_sorted_ind = summary_recomm.tokenizer(df_webtoon)

        recommend_result = {}

        for favorite_webtoon in favorite_webtoons:
            title = favorite_webtoon.webtoon_name

            # 찜목록에 있는 모든 웹툰리스트들과 가장 유사도가 높은 몇가지를 출력
            similar_webtoons = summary_recomm.find_sim_movie_ver2(df_webtoon, overview_sim_sorted_ind, '{}'.format(title), 3)
            results = json.loads(similar_webtoons)
            recommend_result[title] = results
        
        return Response(recommend_result)

class WebtoonScoreViewSet(viewsets.ModelViewSet):
    """
        웹툰 평점 순 추천
        ---
        # 내용
    """
    serializer_class = WebtoonSerializer

    # @api_view(['GET'])
    @authentication_classes([JSONWebTokenAuthentication])
    @permission_classes([IsAuthenticated]) 
    def recomm_score(self, request):
        webtoons = Webtoon.objects.order_by("-webtoon_score")[:10]
        serializer = WebtoonSerializer(webtoons, many=True)
        return Response(serializer.data)

def recomm_media(request):
    pass

class WebtoonRandomViewSet(viewsets.ModelViewSet):
    """
        웹툰 랜덤 추천
    """
    serializer_class = WebtoonSerializer

    # @api_view(['GET'])
    @authentication_classes([JSONWebTokenAuthentication])
    @permission_classes([IsAuthenticated]) 
    def recomm_random(self, request):
        webtoon = Webtoon.objects.order_by("?")[0]
        serializer = WebtoonSerializer(webtoon)
        return Response(serializer.data)
    

class WebtoonOppositionViewSet(viewsets.ModelViewSet):
    """
        웹툰 줄거리 기반 반대 추천
        ---
    """
    serializer_class = WebtoonSerializer

    @authentication_classes([JSONWebTokenAuthentication])
    @permission_classes([IsAuthenticated]) 
    def recomm_opposition(self, request):
        # 로그인 유저의 찜리스트 목록 가져오기
        user_id = get_user_model().objects.values('user_id').filter(username="tester")
        # user_id = get_user_model().objects.values('user_id').filter(username=request.user)
        favorite_webtoons = Webtoon.objects.filter(users_webtoon=user_id[0]['user_id'])
        
        webtoons = Webtoon.objects.all()

        df_webtoon = summary_recomm.to_dataframe(webtoons)
        overview_sim_sorted_ind = summary_recomm.opposition_tokenizer(df_webtoon)

        recommend_result = {}

        for favorite_webtoon in favorite_webtoons:
            title = favorite_webtoon.webtoon_name

            # 찜목록에 있는 모든 웹툰리스트들과 가장 유사도가 높은 몇가지를 출력
            similar_webtoons = summary_recomm.find_sim_movie_ver2(df_webtoon, overview_sim_sorted_ind, '{}'.format(title), 3)
            results = json.loads(similar_webtoons)
            recommend_result[title] = results
        
        return Response(recommend_result)


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


from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder

from rest_framework import status, viewsets
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from webtoons.serializers import WebtoonSerializer
from model import summary_recomm, genre_recomm
from webtoons.models import Webtoon, Genre

from drf_yasg import openapi
import json


class WebtoonOverAllViewSet(viewsets.ModelViewSet):
    """
        웹툰 추천 통합
    """

    serializer_class = WebtoonSerializer

    @authentication_classes([JSONWebTokenAuthentication])
    @permission_classes([IsAuthenticated])   
    def recomm_overall(self, request):
        # # 장르
        # # 사용자의 장르 벡터
        # user_id = get_user_model().objects.values('user_id').filter(username="sadml.faklsdjfklsad")
        # # user_id = get_user_model().objects.values('user_id').filter(username=request.user)
        # favorite_webtoons = Webtoon.objects.filter(favorite_users=user_id[0]['user_id'])
        # serializer = WebtoonSerializer(favorite_webtoons, many=True)
        # webtoon_data = serializer.data

        # user_genres_matrix = genre_recomm.user_to_matrix(webtoon_data)

        # # 웹툰들의 장르 벡터
        # webtoons = Webtoon.objects.all()
        # df_webtoon = genre_recomm.webtoon_to_dataframe(webtoons)
        # genre_mat =  genre_recomm.webtoon_to_matrix(df_webtoon)
        
        # # 각각의 유사도 계산
        # similarity = genre_recomm.cal_similarity(user_genres_matrix, genre_mat)
        
        # # 유사도 순 정렬
        # sorted_similarity = sorted(similarity.items(), reverse=True, key=lambda item: item[1])
        
        # # id값에 해당하는 웹툰 정보 응답
        # result = []
        # for i in range(10):
        #     webtoon = Webtoon.objects.filter(webtoon_number=sorted_similarity[i][0])
        #     serializer = WebtoonSerializer(webtoon[0])
        #     result.append(serializer.data)
       
        # # 작가
        # user_id = get_user_model().objects.values('user_id').filter(username="sadml.faklsdjfklsad")
        # # user_id = get_user_model().objects.values('user_id').filter(username=request.user)
        # favorite_webtoons = Webtoon.objects.filter(favorite_users=user_id[0]['user_id'])
        
        # recommend_result = {}
        # webtoons = Webtoon.objects.all()

        # for favorite_webtoon in favorite_webtoons:
        #     writer = favorite_webtoon.webtoon_writer
        #     already_num = favorite_webtoon.webtoon_number
            
        #     tmp = []

        #     for webtoon in webtoons:
        #         if webtoon.webtoon_writer in writer and webtoon.webtoon_number != already_num:
        #             serializer = WebtoonSerializer(webtoon)
        #             tmp.append(serializer.data)
        #             recommend_result[writer] = tmp

        # 줄거리
        # 로그인 유저의 찜리스트 목록 가져오기
        user_id = get_user_model().objects.values('user_id').filter(username="sadml.faklsdjfklsad")
        # user_id = get_user_model().objects.values('user_id').filter(username=request.user)
        favorite_webtoons = Webtoon.objects.filter(favorite_users=user_id[0]['user_id'])
        
        webtoons = Webtoon.objects.all()

        df_webtoon = summary_recomm.to_dataframe(webtoons)
        overview_sim_sorted_ind = summary_recomm.tokenizer(df_webtoon)

        summmary_result = {}

        for favorite_webtoon in favorite_webtoons:
            title = favorite_webtoon.webtoon_name

            # 찜목록에 있는 모든 웹툰리스트들과 가장 유사도가 높은 몇가지를 출력
            similar_webtoons = summary_recomm.find_sim_movie_ver2(df_webtoon, overview_sim_sorted_ind, '{}'.format(title), 3)

            results = json.loads(similar_webtoons)

            tmp = []
            for result in results:
                webtoon = Webtoon.objects.get(webtoon_number=result['webtoon_number'])        
                serializer = WebtoonSerializer(webtoon)
                tmp.append(serializer.data)

            summmary_result[title] = tmp

        # 평점
        webtoons = Webtoon.objects.order_by("-webtoon_score")[:10]
        score_serializer = WebtoonSerializer(webtoons, many=True)

        # 무작위
        webtoon = Webtoon.objects.order_by("?")[:5]
        serializer = WebtoonSerializer(webtoon, many=True)

        # 반대
        # 로그인 유저의 찜리스트 목록 가져오기
        user_id = get_user_model().objects.values('user_id').filter(username="sadml.faklsdjfklsad")
        # user_id = get_user_model().objects.values('user_id').filter(username=request.user)
        favorite_webtoons = Webtoon.objects.filter(favorite_users=user_id[0]['user_id'])
        
        webtoons = Webtoon.objects.all()

        df_webtoon = summary_recomm.to_dataframe(webtoons)
        overview_sim_sorted_ind = summary_recomm.opposition_tokenizer(df_webtoon)

        opposition_result = {}

        for favorite_webtoon in favorite_webtoons:
            title = favorite_webtoon.webtoon_name

            # 찜목록에 있는 모든 웹툰리스트들과 가장 유사도가 높은 몇가지를 출력
            similar_webtoons = summary_recomm.find_sim_movie_ver2(df_webtoon, overview_sim_sorted_ind, '{}'.format(title), 3)

            results = json.loads(similar_webtoons)

            tmp = []
            for result in results:
                webtoon = Webtoon.objects.get(webtoon_number=result['webtoon_number'])        
                opposition_serializer = WebtoonSerializer(webtoon)
                tmp.append(opposition_serializer.data)

            opposition_result[title] = tmp

        return Response(
            {
                # "장르유사도가 높은": result,
                "작가의 다른 작품": recommend_result,
                "줄거리 유사도가 높은": summmary_result,
                "평점이 높은 순": score_serializer.data,
                "무작위": serializer.data,
                "줄거리 유사도가 낮은": opposition_result,
             })


class WebtoonGenreViewSet(viewsets.ModelViewSet):
    """
        웹툰 장르 벡터와 사용자 장르 벡터 유사도 계산 기반 추천
    """

    serializer_class = WebtoonSerializer

    @authentication_classes([JSONWebTokenAuthentication])
    @permission_classes([IsAuthenticated])   
    def recomm_genre(self, request):
        # 사용자의 장르 벡터
        user_id = get_user_model().objects.values('user_id').filter(username="sadml.faklsdjfklsad")
        # user_id = get_user_model().objects.values('user_id').filter(username=request.user)
        favorite_webtoons = Webtoon.objects.filter(favorite_users=user_id[0]['user_id'])
        serializer = WebtoonSerializer(favorite_webtoons, many=True)
        webtoon_data = serializer.data

        user_genres_matrix = genre_recomm.user_to_matrix(webtoon_data)

        # 웹툰들의 장르 벡터
        webtoons = Webtoon.objects.all()
        df_webtoon = genre_recomm.webtoon_to_dataframe(webtoons)
        genre_mat =  genre_recomm.webtoon_to_matrix(df_webtoon)
        
        # 각각의 유사도 계산
        similarity = genre_recomm.cal_similarity(user_genres_matrix, genre_mat)
        
        # 유사도 순 정렬
        sorted_similarity = sorted(similarity.items(), reverse=True, key=lambda item: item[1])
        
        # id값에 해당하는 웹툰 정보 응답
        result = []
        for i in range(10):
            webtoon = Webtoon.objects.filter(webtoon_number=sorted_similarity[i][0])
            serializer = WebtoonSerializer(webtoon[0])
            result.append(serializer.data)
        return Response(result)


class WebtoonArtistViewSet(viewsets.ModelViewSet):
    """
        웹툰 작가 기반 추천
        ---
    """
    serializer_class = WebtoonSerializer

    @authentication_classes([JSONWebTokenAuthentication])
    @permission_classes([IsAuthenticated])    
    def recomm_artist(self, request):
        user_id = get_user_model().objects.values('user_id').filter(username="sadml.faklsdjfklsad")
        # user_id = get_user_model().objects.values('user_id').filter(username=request.user)
        favorite_webtoons = Webtoon.objects.filter(favorite_users=user_id[0]['user_id'])
        
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
        user_id = get_user_model().objects.values('user_id').filter(username="sadml.faklsdjfklsad")
        # user_id = get_user_model().objects.values('user_id').filter(username=request.user)
        favorite_webtoons = Webtoon.objects.filter(favorite_users=user_id[0]['user_id'])
        
        webtoons = Webtoon.objects.all()

        df_webtoon = summary_recomm.to_dataframe(webtoons)
        overview_sim_sorted_ind = summary_recomm.tokenizer(df_webtoon)

        recommend_result = {}

        for favorite_webtoon in favorite_webtoons:
            title = favorite_webtoon.webtoon_name

            # 찜목록에 있는 모든 웹툰리스트들과 가장 유사도가 높은 몇가지를 출력
            similar_webtoons = summary_recomm.find_sim_movie_ver2(df_webtoon, overview_sim_sorted_ind, '{}'.format(title), 3)

            results = json.loads(similar_webtoons)

            tmp = []
            for result in results:
                webtoon = Webtoon.objects.get(webtoon_number=result['webtoon_number'])        
                serializer = WebtoonSerializer(webtoon)
                tmp.append(serializer.data)

            recommend_result[title] = tmp
        
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
        webtoon = Webtoon.objects.order_by("?")[:5]
        serializer = WebtoonSerializer(webtoon, many=True)
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
        user_id = get_user_model().objects.values('user_id').filter(username="sadml.faklsdjfklsad")
        # user_id = get_user_model().objects.values('user_id').filter(username=request.user)
        favorite_webtoons = Webtoon.objects.filter(favorite_users=user_id[0]['user_id'])
        
        webtoons = Webtoon.objects.all()

        df_webtoon = summary_recomm.to_dataframe(webtoons)
        overview_sim_sorted_ind = summary_recomm.opposition_tokenizer(df_webtoon)

        recommend_result = {}

        for favorite_webtoon in favorite_webtoons:
            title = favorite_webtoon.webtoon_name

            # 찜목록에 있는 모든 웹툰리스트들과 가장 유사도가 높은 몇가지를 출력
            similar_webtoons = summary_recomm.find_sim_movie_ver2(df_webtoon, overview_sim_sorted_ind, '{}'.format(title), 3)

            results = json.loads(similar_webtoons)

            tmp = []
            for result in results:
                webtoon = Webtoon.objects.get(webtoon_number=result['webtoon_number'])        
                serializer = WebtoonSerializer(webtoon)
                tmp.append(serializer.data)

            recommend_result[title] = tmp
        
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


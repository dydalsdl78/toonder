from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render

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


# 사용자 정보가 필요한 항목들--------------------------
# 이건 뭐지?
def recomm_overall(request):
    pass


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
        
        
        return Response(sorted_similarity[:10])


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
            recommend_result[title] = results
        
        return Response(recommend_result)


@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def like(request, webtoon_number):
    if request.user.is_authenticated:
        webtoon = get_object_or_404(Webtoon, pk=webtoon_number)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if webtoon.like_users.filter(pk=request.user.user_id).exists():
        webtoon.like_users.remove(request.user)

    else:
        webtoon.like_users.add(request.user)
    return Response(status=status.HTTP_201_CREATED)


@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])  
def favorite(request, webtoon_number):
    if request.user.is_authenticated:
        webtoon = get_object_or_404(Webtoon, pk=webtoon_number)
        
    if webtoon.favorite_users.filter(pk=request.user.user_id).exists():
        webtoon.favorite_users.remove(request.user)

    else:
        webtoon.favorite_users.add(request.user)
        
    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def like_list(request):
    if request.user.is_authenticated:
        user = request.user
        like_list = user.like_webtoon.all()
        genres = Genre.objects.all()

        webtoon_like_list = list()

        i = 0
        for webtoon in like_list:
            
            webtoon_like = dict()
            genres_names = []
            webtoon_genres = webtoon.genres.all()

            for webtoon_genre in webtoon_genres:
                for genre in genres:
                    genre_name = genre.genre_name

                    if webtoon_genre.id == genre.id:
                        genres_names.append(genre.genre_name)
                        webtoon_genre.id = genre.genre_name
            i += 1

            serializer = WebtoonSerializer(webtoon)
            webtoon_like = serializer.data
            webtoon_like['genres_names'] = genres_names
            webtoon_like_list.append(webtoon_like)

    return Response(webtoon_like_list, status=status.HTTP_202_ACCEPTED)

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def favorite_list(request):
    if request.user.is_authenticated:
        user = request.user
        favorite_list = user.favorite_webtoon.all()
        genres = Genre.objects.all()

        webtoon_favorite_list = list()

        i = 0
        for webtoon in favorite_list:
            webtoon_favorite = dict()
            genres_names = []
            webtoon_genres = webtoon.genres.all()

            for webtoon_genre in webtoon_genres:
                for genre in genres:
                    genre_name = genre.genre_name

                    if webtoon_genre.id == genre.id:
                        genres_names.append(genre.genre_name)
                        webtoon_genre.id = genre.genre_name
            i += 1

            serializer = WebtoonSerializer(webtoon)
            webtoon_favorite = serializer.data
            webtoon_favorite['genres_names'] = genres_names
            webtoon_favorite_list.append(webtoon_favorite)

    return Response(webtoon_favorite_list, status=status.HTTP_202_ACCEPTED)


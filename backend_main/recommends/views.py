from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

from webtoons.serializers import WebtoonSerializer, SummarySerializer
from model import summary_recomm
from webtoons.models import Webtoon, Genre

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
        
        result = {}

        for genre in genres:
            webtoon_genre_ls = []
            genre_name = genre.genre_name

            for webtoon in webtoons[:100]:
                genres = webtoon.genres.all()
                for genre in genres:
                    if genre_name == genre.genre_name and len(webtoon_genre_ls) < 3:
                        serializer = WebtoonSerializer(webtoon)
                        webtoon_genre_ls.append(serializer.data)
                    else:
                        continue
            result[genre_name] = webtoon_genre_ls
                
        return Response(result)    

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


# 웹툰 추천 카드 관련---------------------------------------------
# 사용자 정보가 필요한 항목들--------------------------
def recomm_overall(request):
    pass
def recomm_genre(request):
    # 사용자의 장르 벡터
    # 웹툰들의 장르 벡터
    pass


class WebtoonArtistViewSet(viewsets.ModelViewSet):
    """
        웹툰 작가 기반 추천
        ---
    """
    serializer_class = WebtoonSerializer

    @authentication_classes([JSONWebTokenAuthentication])
    @permission_classes([IsAuthenticated])    
    def recomm_artist(self, request):
        # webtoon_user = settings.AUTH_USER_MODEL.objects.values('id').filter(username=request.data['name'])
        # webtoon_user = settings.AUTH_USER_MODEL.objects.values('id').filter(username=request.user)
        # Favortie 모델에서 가져오기
        # webtoons = Favorite.objects.filter(user_id=webtoon_user[0]['id'])
        # 찜목록에 있는 웹툰의 작가들
        # webtoons.favorites.all()
        # settings.AUTH_USER_MODEL
        # 로그인된 사용자의 정보를 통해 찜목록에 있는 것을 갖고온다.
        # favorite_webtoons = Webtoon.objects.filter(webtoon_writer='찜목록의 작가이름')
        return Response(0)

# 사용자 정보가 필요없는 항목들------------------------
class WebtoonSummaryViewSet(viewsets.ModelViewSet):
    """
        웹툰 줄거리 기반 추천
        ---
        # 내용
            { "title" : "웹툰 제목" }
    """
    serializer_class = WebtoonSerializer

    # @api_view(['POST'])
    @authentication_classes([JSONWebTokenAuthentication])
    @permission_classes([IsAuthenticated]) 
    def recomm_summary(self, request):
        # user_id = get_user_model().objects.values('id').filter(username=request.user)
        # favorite_webtoons = Webtoon.objects.filter(user_id=user_id[0]['id'])

        webtoons = Webtoon.objects.all()

        df_webtoon = summary_recomm.to_dataframe(webtoons)
        overview_sim_sorted_ind = summary_recomm.tokenizer(df_webtoon)
        title = request.data['title']
        # title = '학사재생'
        # 찜목록에 있는 모든 웹툰리스트들과 가장 유사도가 높은 몇가지를 출력해야함
        similar_webtoons = summary_recomm.find_sim_movie_ver2(df_webtoon, overview_sim_sorted_ind, '{}'.format(title), 10)
        results = json.loads(similar_webtoons)
        return Response(results)

class WebtoonScoreViewSet(viewsets.ModelViewSet):
    """
        웹툰 평점 순 추천
        ---
        # 내용
    """
    # queryset = Webtoon.objects.all() 
    serializer_class = WebtoonSerializer

    # @api_view(['GET'])
    @authentication_classes([JSONWebTokenAuthentication])
    @permission_classes([IsAuthenticated]) 
    def recomm_score(self, request):
        webtoons = Webtoon.objects.order_by("-webtoon_score")[:10]
        # 시리얼라이즈
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
    
def recomm_opposition(request):
    # 어떤기준으로 완전 반대되는 추천??
    pass

# def 장르 10개씩 평점순


# 유저 좋아요, 찜목록 리스트 관련----------------------------------

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


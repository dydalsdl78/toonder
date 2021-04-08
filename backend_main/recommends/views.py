from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from webtoons.serializers import WebtoonSerializer
from model import summary_recomm, genre_recomm
from webtoons.models import Webtoon, Genre

import random
import json
import io


class WebtoonOverAllViewSet(viewsets.ModelViewSet):
    """
        웹툰 추천 통합
    """
    serializer_class = WebtoonSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def recomm_overall(self, request):
    
    # 사용자의 좋아요 리스트에 있는 웹툰 목록
        user = request.user
        user_id = get_user_model().objects.values('user_id').filter(username=user.username)
        favorite_webtoons = Webtoon.objects.filter(like_users=user_id[0]['user_id'])

    # 웹툰 전체 목록
        webtoons = Webtoon.objects.all()

    # 1. 사용자 장르 벡터와 웹툰 장르 벡터의 유사도가 높은 순서

        # 사용자의 장르 벡터
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
        genre_result = []
        for i in range(10):
            webtoon = Webtoon.objects.filter(webtoon_number=sorted_similarity[i][0])
            serializer = WebtoonSerializer(webtoon[0])
            genre_result.append(serializer.data)

    # 2. 좋아요한 웹툰의 작가가 쓴 다른 웹툰들
        artists_result = []
        
        for favorite_webtoon in favorite_webtoons:
            writer = favorite_webtoon.webtoon_writer
            # 이미 존재하는 웹툰의 id값
            already_num = favorite_webtoon.webtoon_number
            
            for webtoon in webtoons:
                # 좋아요한 웹툰의 작가가 그린 다른 웹툰 and 이미 좋아요 한 웹툰
                if webtoon.webtoon_writer in writer and webtoon.webtoon_number != already_num:
                    serializer = WebtoonSerializer(webtoon)
                    # json 형태로 변환
                    artist_json = JSONRenderer().render(serializer.data)
                    artist_stream = io.BytesIO(artist_json)
                    artist_data = JSONParser().parse(artist_stream)
                    # key-value 추가
                    artist_data['favorite_writer'] = writer

                    artists_result.append(artist_data)


    # 3. 좋아요한 웹툰과 줄거리 유사도 높은 웹툰들
        df_webtoon = summary_recomm.to_dataframe(webtoons)
        overview_sim_sorted_ind = summary_recomm.tokenizer(df_webtoon)

        summmary_result = []

        for favorite_webtoon in favorite_webtoons:
            title = favorite_webtoon.webtoon_name

            # 찜목록에 있는 모든 웹툰리스트들과 가장 유사도가 높은 3개를 출력
            similar_webtoons = summary_recomm.find_sim_movie_ver2(df_webtoon, overview_sim_sorted_ind, '{}'.format(title), 3)

            similar_webtoons_json = json.loads(similar_webtoons)

            for result in similar_webtoons_json:
                webtoon = Webtoon.objects.get(webtoon_number=result['webtoon_number'])        
                serializer = WebtoonSerializer(webtoon)
                # json 형태로 변환
                summary_json = JSONRenderer().render(serializer.data)
                summary_stream = io.BytesIO(summary_json)
                summary_data = JSONParser().parse(summary_stream)
                # key-value 추가
                summary_data['similar_webtoon'] = title

                summmary_result.append(summary_data)

    # 4. 다른 사람들이 높게 평가한 웹툰들
        score_webtoons = Webtoon.objects.order_by("-webtoon_score")[:10]
        score_serializer = WebtoonSerializer(score_webtoons, many=True)
        score_result = score_serializer.data

    # 5. 무작위 추천 웹툰(계속해서 비슷한 것만 나오게 하는 것 방지)
        random_webtoon = Webtoon.objects.order_by("?")[:5]
        random_serializer = WebtoonSerializer(random_webtoon, many=True)
        random_result = random_serializer.data

    # 6. 좋아요한 웹툰과 줄거리 유사가 낮은 웹툰들
        df_webtoon = summary_recomm.to_dataframe(webtoons)
        overview_sim_sorted_ind = summary_recomm.opposition_tokenizer(df_webtoon)

        opposition_result = []

        for favorite_webtoon in favorite_webtoons:
            title = favorite_webtoon.webtoon_name

            # 찜목록에 있는 모든 웹툰리스트들과 가장 유사도가 낮은 30개를 출력
            unsimilar_webtoons = summary_recomm.find_sim_movie_ver2(df_webtoon, overview_sim_sorted_ind, '{}'.format(title), 30)
            results = json.loads(unsimilar_webtoons)

            # 30개중 3개씩 랜덤추출
            results = random.sample(results, 3)

            for result in results:
                webtoon = Webtoon.objects.get(webtoon_number=result['webtoon_number'])        
                opposition_serializer = WebtoonSerializer(webtoon)
                # json 형태로 변환
                opposition_json = JSONRenderer().render(opposition_serializer.data)
                opposition_stream = io.BytesIO(opposition_json)
                opposition_data = JSONParser().parse(opposition_stream)
                # key-value 추가
                opposition_data['opposition_webtoon'] = title

                opposition_result.append(opposition_data)
    
    # 응답
        return Response(
            [
                {"이런 장르의 작품을 좋아하시네요!": genre_result},
                {"좋아하는 작가의 다른 작품": artists_result},
                {"좋아하는 작품과 줄거리 유사한": summmary_result},
                {"다른 사람들이 좋은 평가를 한": score_result},
                {"이런건 어떤가요?": random_result},
                {"평소에는 보지 않지만 어떠세요?": opposition_result},
            ])


class WebtoonStyleViewSet(viewsets.ModelViewSet):
    """
        웹툰 그림체 추천 통합
    """

    serializer_class = WebtoonSerializer

    def recomm_style(self, request):
        webtoons = Webtoon.objects.order_by("scale_loss")
        # 비슷한 그림체 10개
        style_similar_webtoon = webtoons[1:16]
        # 다른 그림체 10개
        style_unsimilar_webtoon = webtoons[len(webtoons)-16:]
        serializer_similar = WebtoonSerializer(style_similar_webtoon, many=True)
        serializer_unsimilar = WebtoonSerializer(style_unsimilar_webtoon, many=True)

        return Response([
                {"그림체 비슷한 10개": serializer_similar.data},
                {"그림체 다른 10개": serializer_unsimilar.data}
                ])


class LikeViewSet(viewsets.ModelViewSet):
    """
        좋아요 기능
    """
    serializer_class = WebtoonSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]   

    def like(self, request, webtoon_number):
        print(request.user)
        if request.user.is_authenticated:
            webtoon = get_object_or_404(Webtoon, pk=webtoon_number)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if webtoon.like_users.filter(pk=request.user.user_id).exists():
            webtoon.like_users.remove(request.user)

        else:
            webtoon.like_users.add(request.user)
        return Response(status=status.HTTP_201_CREATED)


class FavoriteViewSet(viewsets.ModelViewSet):
    """
        찜하기 기능
    """
    serializer_class = WebtoonSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]


    def favorite(self, request, webtoon_number):
        print(request.user)
        if request.user.is_authenticated:
            webtoon = get_object_or_404(Webtoon, pk=webtoon_number)
            
        if webtoon.favorite_users.filter(pk=request.user.user_id).exists():
            webtoon.favorite_users.remove(request.user)

        else:
            webtoon.favorite_users.add(request.user)
            
        return Response(status=status.HTTP_201_CREATED)


class LikeListViewSet(viewsets.ModelViewSet):
    """
        좋아요 리스트 응답
    """
    serializer_class = WebtoonSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]   


    def like_list(self, request):
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

class FavoriteListViewSet(viewsets.ModelViewSet):
    """
        찜하기 리스트 응답
    """
    serializer_class = WebtoonSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]   

    def favorite_list(self, request):
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


from random import sample

from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated

from accounts.models import User
from .models import Webtoon, Genre
from .serializers import WebtoonSerializer, GenreSerializer

class MainViewSet(viewsets.ModelViewSet):
# @api_view(['GET'])
    """
        메인 페이지: 장르별 10개씩 출력
    """

    serializer_class = WebtoonSerializer
    
    def main(self, request):
        # [{ "1번장르" : [웹툰1, 웹툰1, 웹툰3]}, {"2번장르" : [웹툰4, 웹툰5, 웹툰6] }]
        results = dict()
        genres = Genre.objects.all()
        genre_ids = list(genres.values('id'))
        
        for genre_id in sample(genre_ids, 8):
            # print(list(genres[genre_id['id'] - 1].webtoons.all().order_by('-webtoon_score')[:10].values()))
            results[genres[genre_id['id'] - 1].genre_name] = list(genres[genre_id['id'] - 1].webtoons.all().order_by('-webtoon_score')[:10].values())

        # print(results.keys())

        return Response(results, status=status.HTTP_200_OK)


class SearchViewSet(viewsets.ModelViewSet):
    """
        웹툰 검색 결과 출력
        --
        { 
            "keyword": "키워드" 
        }
    """

    serializer_class = WebtoonSerializer
    # @api_view(['GET'])
    # @authentication_classes([JSONWebTokenAuthentication])
    # @permission_classes([IsAuthenticated])
    def search_keyword(self, request):
        keyword = request.data['keyword']
        
        webtoons = Webtoon.objects.filter(
            webtoon_name__contains=keyword
        ).union(Webtoon.objects.filter(
            overview__contains=keyword
        ))

        # 장르 데이터 추가하는 코드
        genres = Genre.objects.all()
        
        webtoon_list = list()
        serializer = WebtoonSerializer(webtoons, many=True)
        print(webtoons)
        for webtoon in webtoons:
            print(webtoon)
            print(webtoon.genres.all())

            webtoon_info = dict()
            genres_names = []
            webtoon_genres = webtoon.genres.all()

            for webtoon_genre in webtoon_genres:
                for genre in genres:
                    genre_name = genre.genre_name

                    if webtoon_genre.id == genre.id:
                        genres_names.append(genre.genre_name)


            serializer = WebtoonSerializer(webtoon)
            webtoon_info = serializer.data
            webtoon_info['genres_names'] = genres_names
            webtoon_list.append(webtoon_info)

        return Response(webtoon_list, status=status.HTTP_200_OK)



class DetailViewSet(viewsets.ModelViewSet):
# @api_view(['GET'])
    """
        웹툰 상세 페이지
    """

    serializer_class = WebtoonSerializer
    # @api_view(['GET'])
    def webtoon_detail(self, request, webtoon_pk):
        webtoon = get_object_or_404(Webtoon, pk=webtoon_pk)

        webtoon_serializer = WebtoonSerializer(webtoon)

        # 장르 데이터 추가하는 코드
        genres = Genre.objects.all()
        

        webtoon_info = dict()
        genres_names = []
        webtoon_genres = webtoon.genres.all()

        for webtoon_genre in webtoon_genres:
            for genre in genres:
                genre_name = genre.genre_name

                if webtoon_genre.id == genre.id:
                    genres_names.append(genre.genre_name)


        serializer = WebtoonSerializer(webtoon)
        webtoon_info = serializer.data
        webtoon_info['genres_names'] = genres_names


        return Response(webtoon_info, status=status.HTTP_200_OK)
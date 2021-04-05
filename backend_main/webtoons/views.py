from random import sample

from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Webtoon, Genre
from .serializers import WebtoonSerializer


@api_view(['GET'])
def index(request):
    # [{ "1번장르" : [웹툰1, 웹툰1, 웹툰3]}, {"2번장르" : [웹툰4, 웹툰5, 웹툰6] }]
    results = dict()
    genres = Genre.objects.all()
    genre_ids = list(genres.values('id'))
    
    for genre_id in sample(genre_ids, 8):
        # print(list(genres[genre_id['id'] - 1].webtoons.all().order_by('-webtoon_score')[:10].values()))
        results[genres[genre_id['id'] - 1].genre_name] = list(genres[genre_id['id'] - 1].webtoons.all().order_by('-webtoon_score')[:10].values())

    # print(results.keys())

    return Response(results, status=status.HTTP_200_OK)


@api_view(['GET'])
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes([IsAuthenticated])
def search_keyword(request):
    keyword = request.data['keyword']
    
    webtoons = Webtoon.objects.filter(
        webtoon_name__contains=keyword
    ).union(Webtoon.objects.filter(
        overview__contains=keyword
    ))

    webtoon_serializer = WebtoonSerializer(webtoons, many=True)

    return Response(webtoon_serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def webtoon_detail(request, webtoon_pk):
    webtoon = get_object_or_404(Webtoon, pk=webtoon_pk)

    webtoon_serializer = WebtoonSerializer(webtoon)

    return Response(webtoon_serializer.data, status=status.HTTP_200_OK)
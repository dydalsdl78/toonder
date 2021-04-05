from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Webtoon, Genre
from .serializers import WebtoonSerializer, GenreSerializer

def search_keyword(request):
    keyword = request.data['keyword']
    print(keyword)

    return Response(status=status.HTTP_200_OK)

# 장르별 웹툰 목록
# class WebtoonMainViewSet(viewsets.ModelViewSet):
#     """
#         웹툰 메인 장르별 목록 출력
#         ---
#     """
#     serializer_class = WebtoonSerializer

#     def webtoon_main(self, request):
#         genres = Genre.objects.all()
#         webtoons = Webtoon.objects.all()
#         for i in genres:
#             print(i.id)
#         result = {}
#         for w in webtoons[:5]:
#             serializer = GenreSerializer(w.genres, many=True)
#             print(serializer.data)
#         # for genre in genres[:5]:
#         #     webtoon_genre_ls = []
#         #     genre_name = genre.genre_name
#         #     print(genre_name)
#         #     for webtoon in webtoons:
#         #         print(webtoon.webtoon_name)
#         #         w_genres = webtoon.genres.all()
#         #         for w_genre in w_genres:
#         #             if genre_name == w_genre.genre_name and len(webtoon_genre_ls) < 9:
#         #                 serializer = WebtoonSerializer(webtoon)
#         #                 webtoon_genre_ls.append(serializer.data)
#         #     result[genre_name] = webtoon_genre_ls
                
#         return Response(0)    

# 전체 웹툰 리스트------------------------------------------------
# class WebtoonListViewSet(viewsets.ModelViewSet):
#     """
#         웹툰 전체 목록 출력
#         ---
#     """
#     serializer_class = WebtoonSerializer

#     # @api_view(['GET'])
#     def webtoon_list(self, request):
#         webtoons = Webtoon.objects.all()
#         serializer = WebtoonSerializer(webtoons, many=True)
#         return Response(serializer.data)
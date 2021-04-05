from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Webtoon
from .serializers import WebtoonSerializer


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
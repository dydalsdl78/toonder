from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view


def search_keyword(request):
    keyword = request.data['keyword']
    print(keyword)

    return Response(status=status.HTTP_200_OK)
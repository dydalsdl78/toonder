from django.shortcuts import render
from .models import Webtoon
from .serializers import WebtoonSerializer


# 

def index(request):
    webtoons = Webtoon.objects.all()


    print(type(webtoons))
    print(webtoons) # 전체 웹툰의 QuerySet
    print(webtoons[1]) # 해당 웹툰의 QuerySet
    print(webtoons[1].webtoon_name) # 해당 웹툰의 이름

    return 0
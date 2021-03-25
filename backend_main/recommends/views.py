from django.shortcuts import render
from .models import Webtoon
from .serializers import WebtoonSerializer

def index(request):
    webtoons = Webtoon.objects.all()


    print(type(webtoons))
    print(webtoons) # 전체 웹툰의 QuerySet
    print(webtoons[1]) # 해당 웹툰의 QuerySet
    print(webtoons[1].webtoon_name) # 해당 웹툰의 이름

    return 0

# 전체 웹툰 리스트------------------------------------------------
def webtoon_list(request):
    pass


# 웹툰 추천 카드 관련---------------------------------------------
# 사용자 정보가 필요한 항목들--------------------------
def recomm_overall(request):
    pass
def recomm_genre(request):
    pass
def recomm_artist(request):
    pass

# 사용자 정보가 필요없는 항목들------------------------
def recomm_score(request):
    pass
def recomm_media(request):
    pass
def recomm_random(request):
    pass
def recomm_opposition(request):
    pass




# 유저 좋아요, 찜목록 리스트 관련----------------------------------

# 유저 좋아요 리스트 & 추가하기
def likes_list_create(request):
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


from django.urls import path
from . import views
from .views import WebtoonOverAllViewSet, WebtoonStyleViewSet, LikeViewSet, FavoriteViewSet, LikeListViewSet, FavoriteListViewSet

urlpatterns = [

    # 웹툰 추천 카드 주소
    path('recomm_overall/', WebtoonOverAllViewSet.as_view({"get":"recomm_overall"})),
    path('recomm_style/', WebtoonStyleViewSet.as_view({"get":"recomm_style"})),

    # 유저 좋아요, 찜목록 리스트 관련 주소들
    path('like/<int:webtoon_number>/', LikeViewSet.as_view({"post": "like"}), name='like'),
    path('like/', LikeListViewSet.as_view({"get":"like_list"}), name='like_list'),
    path('favorite/<int:webtoon_number>/', FavoriteViewSet.as_view({"post":"favorite"}), name='favorite'),
    path('favorite/', FavoriteListViewSet.as_view({"get":"favorite_list"}), name='favorite_list'),
]

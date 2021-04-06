from django.urls import path
from . import views
from .views import WebtoonSummaryViewSet, WebtoonMainViewSet, WebtoonArtistViewSet, WebtoonScoreViewSet, WebtoonListViewSet, WebtoonRandomViewSet

urlpatterns = [
    path('', WebtoonMainViewSet.as_view({"get": "webtoon_main"})),

    #전체 웹툰 리스트
    path('webtoon_list/', WebtoonListViewSet.as_view({"get": "webtoon_list"})),

    # 웹툰 추천 카드 관련 주소들
    path('recomm_overall/', views.recomm_overall),
    path('recomm_genre/', views.recomm_genre),
    path('recomm_artist/', WebtoonArtistViewSet.as_view({"get": "recomm_artist"})),
    path('recomm_summary/', WebtoonSummaryViewSet.as_view({"post": "recomm_summary"})),
    path('recomm_score/', WebtoonScoreViewSet.as_view({"get": "recomm_score"})),
    path('recomm_media/', views.recomm_media),
    path('recomm_random/', WebtoonRandomViewSet.as_view({"get": "recomm_random"})),
    path('recomm_opposition/', views.recomm_opposition),

    # 유저 좋아요, 찜목록 리스트 관련 주소들
    path('like/<int:webtoon_number>', views.like, name='like'),
    path('like/', views.like_list, name='like_list'),
    path('favorite/<int:webtoon_number>', views.favorite, name='favorite'),
    path('favorite/', views.favorite_list, name='favorite_list'),
]

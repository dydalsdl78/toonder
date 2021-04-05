from django.urls import path
from . import views
from .views import WebtoonSummaryViewSet, WebtoonGenreViewSet, WebtoonOppositionViewSet, WebtoonArtistViewSet, WebtoonScoreViewSet, WebtoonRandomViewSet

urlpatterns = [

    # 웹툰 추천 카드 관련 주소들
    path('recomm_overall/', views.recomm_overall),
    path('recomm_genre/', WebtoonGenreViewSet.as_view({"get": "recomm_genre"})),
    path('recomm_artist/', WebtoonArtistViewSet.as_view({"get": "recomm_artist"})),
    path('recomm_summary/', WebtoonSummaryViewSet.as_view({"get": "recomm_summary"})),
    path('recomm_score/', WebtoonScoreViewSet.as_view({"get": "recomm_score"})),
    path('recomm_media/', views.recomm_media),
    path('recomm_random/', WebtoonRandomViewSet.as_view({"get": "recomm_random"})),
    path('recomm_opposition/', WebtoonOppositionViewSet.as_view({"get": "recomm_opposition"})),

    # 유저 좋아요, 찜목록 리스트 관련 주소들
    path('likes/', views.likes_list_create),
    path('likes/<int:likes_pk>', views.likes_delete),
    path('favorite/', views.favorite_list_create),
    path('favorite/<int:favorite_pk>', views.favorite_delete),
]

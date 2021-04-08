from django.urls import path

from .views import MainViewSet, SearchViewSet, DetailViewSet


urlpatterns = [
    path('main/', MainViewSet.as_view({"get": "main"})),
    path('search/', SearchViewSet.as_view({"post" : "search_keyword"})),
    path('detail/<int:webtoon_pk>/', DetailViewSet.as_view({ "get" : "webtoon_detail"})),
]

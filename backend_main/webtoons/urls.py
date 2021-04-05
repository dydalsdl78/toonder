from django.urls import path
from . import views


urlpatterns = [
    path('search/', views.search_keyword),
    path('detail/<int:webtoon_pk>/', views.webtoon_detail),
]

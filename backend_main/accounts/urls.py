from django.urls import path
from . import views

from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token


urlpatterns = [
    path('signup/', views.signup),
    path('api-token-auth/', obtain_jwt_token),          # 로그인
    path('api-token-refresh/', refresh_jwt_token),      # token이 필요한 행위를 하기 전, 리프레쉬 요청을 통해 우선 리프레쉬를 하고
                                                        # 리프레쉬에 성공하면 리프레쉬 된 새로운 토큰으로 각각의 요청을 해야한다

    path('get_userinfo/', views.get_userinfo),                   # 유저정보 얻기
    path('modify/profile/', views.modify_profile),      # 유저정보 수정
    path('change/password', views.change_password),     # 비밀번호 변경

    path('change/profile/', views.change_profile),      # post맨으로 실험하는 경로
    path('modify/password', views.modify_password),     # post맨으로 실험하는 경로
]

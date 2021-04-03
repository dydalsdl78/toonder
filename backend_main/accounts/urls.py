from django.urls import path
from . import views

from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token

urlpatterns = [
    # path('', views.login),
    path('signup/', views.signup),
    path('change/profile/', views.change_profile),
    path('modify/password', views.modify_password),
    path('api-token-auth/', obtain_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),
]

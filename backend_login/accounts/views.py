from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer


def login(request):
    pass


@api_view(['POST'])
def signup(request):
    password = request.data.get('password')

    if not password == request.data.get('passwordConfirmation'):
        return Response(
            { 'error': '비밀번호가 일치하지 않습니다.'},
        )

    userserial = UserSerializer(data=request.data)

    if userserial.is_valid(raise_exception=True):
        user = userserial.save()
        user.set_password(password)
        user.save()
        return Response(userserial.data, status=status.HTTP_201_CREATED)
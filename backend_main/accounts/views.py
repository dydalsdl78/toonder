from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

# from .models import User
from .serializers import UserSerializer, ChangeUserSerializer, ChangePasswordSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated

# from django.utils.crypto import ( pbkdf2, get_random_string )

# from django.contrib.auth import update_session_auth_hash

# def login(request):
#     pass


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


@api_view(['PUT'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def change_profile(request):
    user = get_object_or_404(get_user_model(), pk=request.user.user_id)

    if user.check_password(request.data['password']):

        datas = dict()

        if request.data.get('username'):
            datas['username'] = request.data['username']
        else:
            datas['username'] = user.username

        ##### 프로필 이미지 불러오기에 오류가 있음
        ##### backend_login에 있던 것을 그대로 main으로 옮겨와서 그런 것으로 생각됨
        
        # if request.data.get('profile_image'):
        #     datas['profile_image'] = request.data['profile_image']
        # else:
        #     datas['profile_image'] = user.profile_image

        userserial = ChangeUserSerializer(user, data=datas)
        # userserial = ChangeUserSerializer(user, data={
        #     'username': request.data['username'],
        #     'profile_image': request.data['profile_image']
        # })

        if userserial.is_valid(raise_exception=True):
            # if request.data['username']:
            #     userserial.data['username'] = request.data['username']
            # if request.data['profile_image']:
            #     userserial.data['profile_image'] = request.data['profile_image']
            user = userserial.save()
            user.save()
            return Response({ '유저 정보가 업데이트 됐습니다' }, status=status.HTTP_200_OK)
        
        return Response({'이미 존재하는 유저 이름입니다'})
    
    return Response({ '비밀번호 불일치': '현재 비밀번호가 틀렸습니다' })


@api_view(['PUT'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def modify_password(request):
    user = get_object_or_404(get_user_model(), pk=request.user.user_id)

    if user.check_password(request.data['current_password']):

        if request.method == 'PUT':
            userserial = ChangePasswordSerializer(user, data={
                'password': request.data['new_password']
            })
            if userserial.is_valid(raise_exception=True):
                user = userserial.save()
                user.set_password(request.data['new_password'])
                user.save()
                return Response({ '비밀번호가 변경되었습니다' }, status=status.HTTP_200_OK)
        else:
            # 회원 탈퇴가 들어갈 예정
            # user.delete() 하면 될 듯
            # return Response({ '회원탈퇴': '성공' })
            pass
        return Response({ '데이터 유효성': '유효하지 않습니다' })

    return Response({ '비밀번호 불일치': '현재 비밀번호가 틀렸습니다' })

    # print('######################')
    # user = request.user

    # print(user)

    # print(user.check_password(request.data['current_password']))
    # print(user.check_password('하나둘셋야'))



    # infos = user.password.split("$")
    # print(infos)

    # current_password = request.data['current_password']

    # print('########################')
    # current_password = pbkdf2(current_password, infos[2], infos[1])

    # print(current_password)
    # print('########################')
    # print(user.password)


    
    # print(request.data)
    # print('######################')
    # print(request.user.username)
    # print(request.user.password)
    # print('######################')

    # userserializer = UserSerializer(data=request.user)
    # print('######################')
    # print(userserializer)
    # print('######################')
    # print(userserializer.data)
    # print('######################')

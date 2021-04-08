from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer, ChangeUserSerializer, ChangePasswordSerializer


@api_view(['POST'])
def signup(request):
    password = request.data.get('password')

    # 프론트에서도 Confirmation을 확인해서 1차적으로 걸러내지만,
    # 만약 다른 방법으로 시도했을 때 일치하지 않으면 회원가입하지 못하도록
    if not password == request.data.get('passwordConfirmation'):
        return Response(
            { 'failed': '비밀번호가 일치하지 않습니다.' },
        )

    userserial = UserSerializer(data=request.data)

    if userserial.is_valid(raise_exception=True):
        user = userserial.save()
        user.set_password(password)
        user.save()
        return Response(userserial.data, status=status.HTTP_201_CREATED)


# 유저 정보(username)를 얻는 곳
# Headers에 JWT를 보내줘야 한다
@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def get_userinfo(request):
    user = get_object_or_404(get_user_model(), pk=request.user.user_id)

    return Response({
        'username': user.username,
        'email': user.email,
    }, status=status.HTTP_200_OK)


# 유저 정보(유저네임, 프로필 이미지, 비밀번호 등)를 변경하기 전에 비밀번호 검증하기 위해 확인하는 곳
# request.data (body)에 { 'password': 확인을 위해 입력받은 현재 패스워드 }로 보내줘야 한다
@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def certify_password(request):
    user = get_object_or_404(get_user_model(), pk=request.user.user_id)

    if user.check_password(request.data['password']):
        return Response({ 'accomplished': '검증완료' }, status=status.HTTP_202_ACCEPTED)

    # 비밀번호 검증에 실패하면 catch의 error.data에 반환되는 부분
    return Response({ 'failed': '현재 비밀번호가 틀렸습니다.' })


# certify_password로 비밀번호가 확인 되면 유저 정보를 수정하는 곳
# request data에 { 'username': 바꿀 유저네임, 'profile_image': 바꿀 이미지 }로 보내줘야 한다
@api_view(['PUT'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def modify_profile(request):
    user = get_object_or_404(get_user_model(), pk=request.user.user_id)

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

    if userserial.is_valid(raise_exception=True):
        user = userserial.save()
        user.save()
        return Response({ 'accomplished': '유저 정보를 업데이트 했습니다.' }, status=status.HTTP_200_OK)

    return Response({ 'failed': '이미 사용 중인 유저 이름입니다.' })


# certify_password로 비밀번호가 확인 되면 비밀번호를 바꾸는 곳
# request.data에 { 'password': 바꿀 비밀번호 }로 보내줘야 한다
@api_view(['PUT', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = get_object_or_404(get_user_model(), pk=request.user.user_id)

    if request.method == 'PUT':
        userserial = ChangePasswordSerializer(user, data={
            'password': request.data['password']
        })
        if userserial.is_valid(raise_exception=True):
            user = userserial.save()
            user.set_password(request.data['password'])
            user.save()
            return Response({ 'accomplished': '비밀번호를 변경 했습니다.' }, status=status.HTTP_200_OK)
    else: 
        user.delete()
        return Response({ 'accomplished': '성공적으로 탈퇴 되었습니다.' })

    return Response({ 'failed': '유효하지 않습니다.' })

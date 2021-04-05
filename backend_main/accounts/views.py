from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .serializers import UserSerializer, ChangeUserSerializer, ChangePasswordSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated


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

    # 우선 로그인 때 사용한 email은 재활용하고,
    # username을 받아오기 위함
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

    # 비밀번호 검증에 실패하면 catch에 error.data에 반환되는 부분
    # error.data['failed'] 하면 재활용 가능할지도
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
# 회원탈퇴도 이쪽에 넣을 예정
# request.data에 { 'password': 바꿀 비밀번호 }로 보내줘야 한다
@api_view(['PUT'])
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
        # 회원 탈퇴 아직 테스트 안 해봄
        user.delete()
        return Response({ 'accomplished': '성공적으로 탈퇴 되었습니다.' })

    return Response({ 'failed': '유효하지 않습니다.' })


##########################################################################
# postman 테스트를 위해 남겨둔 코드. 이후 프론트엔드 실행이 되면 제거 예정
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

        # print('##################')
        # print(user.username)

        ##### 프로필 이미지 불러오기에 오류가 있음
        ##### backend_login에 있던 것을 그대로 main으로 옮겨와서 그런 것으로 생각됨
        
        # if request.data.get('profile_image'):
        #     datas['profile_image'] = request.data['profile_image']
        # else:
        #     datas['profile_image'] = user.profile_image


        # print('##################')
        # print(user.profile_image)
        

        userserial = ChangeUserSerializer(user, data=datas)
        # userserial = ChangeUserSerializer(user, data={
        #     'username': request.data['username'],
        #     'profile_image': request.data['profile_image']
        # })

        # print('######################')
        # print(userserial)


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


# postman 테스트를 위해 남겨둔 코드. 이후 프론트엔드 실행이 되면 제거 예정
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

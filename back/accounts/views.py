from django.shortcuts import get_object_or_404, get_list_or_404, redirect
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import ProfileSerializer
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()

# Create your views here.
@api_view(['GET'])
def get_profile(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    serializer = ProfileSerializer(user)
    return Response(serializer.data)

@api_view(['GET'])
def get_user_info(request):
    user = request.user
    if not user.is_authenticated:
        return Response({'error': '인증된 사용자가 아닙니다.'}, status=401)
    serializer = ProfileSerializer(user)
    return Response(serializer.data)

@api_view(['POST'])
# @csrf_exempt  # 개발용, 실제 배포에서는 사용하지 않는 것이 좋습니다.
def follow(request, user_pk):
    try:
        to_user = User.objects.get(pk=user_pk)
        if request.user == to_user:
            return HttpResponseBadRequest('자기 자신을 팔로우할 수 없습니다.')

        # 팔로우 상태를 체크합니다.
        if request.user.followings.filter(pk=to_user.pk).exists():
            # 이미 팔로우하고 있다면 팔로우를 취소합니다.
            request.user.followings.remove(to_user)
            return JsonResponse({'message': '팔로우가 취소되었습니다.', 'is_following': False}, status=200)
        else:
            # 팔로우하지 않았다면 새로운 팔로우를 추가합니다.
            request.user.followings.add(to_user)
            return JsonResponse({'message': '팔로우 성공!', 'is_following': True}, status=201)

    except User.DoesNotExist:
        return HttpResponseBadRequest('해당 사용자가 존재하지 않습니다.')

    except Exception as e:
        return HttpResponse(str(e), status=500)
    

# 팔로우 하는 유저 목록 불러오기
@api_view(['GET'])
@csrf_exempt
def get_followings(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    if not request.user.is_authenticated:
        return HttpResponseBadRequest('로그인이 필요한 기능입니다.')
    try:
        # 사용자가 팔로우하는 사람들의 목록을 가져옵니다.
        followings = user.followings.all()

        # 팔로우하는 사람들의 정보를 리스트로 만듭니다.
        followings_list = list(followings.values('id', 'username', 'nickname', 'profile_img_url'))

        # 요청한 사용자의 정보도 포함합니다.
        # my_info = {
        #     'userId': request.user.id,
        #     'nickname': request.user.nickname,
        # }

        return JsonResponse({'followings': followings_list}, status=200)

    except ObjectDoesNotExist:
        return HttpResponseBadRequest('사용자 정보를 찾을 수 없습니다.')

    except Exception as e:
        return HttpResponse(str(e), status=500)


    
@api_view(['GET'])
def get_user_obj(request):
    user = request.user
    # print(user.id, user.nickname)
    if user.is_authenticated:
        serializer =  ProfileSerializer(user)
        # print('if: ', user.id, user.nickname)
        return Response(serializer.data)
    else:
        # print('else: ', user.id, user.nickname)
        return Response({'detail': 'Invalid token or user not found'}, status=400)

    
    
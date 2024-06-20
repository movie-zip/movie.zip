from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Category
from movies.models import Movie
from .serializers import CategoryListSerializer, CategorySerializer

User = get_user_model()
@api_view(['GET', 'POST'])       # category 생성(완) / 해당 유저의 리스트 조회(완)
def category_list(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    if request.method == 'GET':
        categories = get_list_or_404(Category, user=user)
        serializer = CategoryListSerializer(categories, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        category_name = request.data.get('name', '')
        if len(category_name) > 30:
            return Response({"error": "최대 30자까지 입력 가능합니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = CategoryListSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

# 특정 카테고리 수정, 삭제, 카테고리 detail 조회 (다 완)
@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, category_pk):
    category = get_object_or_404(Category, pk=category_pk)
    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = CategorySerializer(
            category, data=request.data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST', 'DELETE'])       
def category_update(request, category_pk, movie_pk):        # 특정 카테고리에 영화 추가/삭제(완)
    category = get_object_or_404(Category, pk=category_pk)
    movie = get_object_or_404(Movie, pk=movie_pk)
    
    if request.method == 'POST':
        # 이미 추가된 영화인지 확인
        if category.movies.filter(pk=movie_pk).exists():
            return Response({"error": "이미 추가된 영화입니다."}, status=status.HTTP_400_BAD_REQUEST)

        # "Category1"인 경우 영화 추가 로직
        if category.name == "Category1":
            if category.movies.count() >= 5:
                # 이미 5개의 영화가 있다면 추가하지 않음
                return Response({"error": "최대 5개의 영화만 추가할 수 있습니다."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # 5개 미만일 경우에만 영화 추가
                category.movies.add(movie)
                category.save()
                return Response({"message": "영화가 성공적으로 추가되었습니다."}, status=status.HTTP_201_CREATED)
        else:
            # Category1이 아닌 다른 카테고리인 경우 영화 추가
            category.movies.add(movie)
            category.save()
            return Response({"message": "영화가 성공적으로 추가되었습니다."}, status=status.HTTP_201_CREATED)
    
    elif request.method == 'DELETE':
        # 영화 삭제 로직 (모든 카테고리에 적용)
        if movie in category.movies.all():
            category.movies.remove(movie)
            category.save()
            return Response({"message": "영화가 성공적으로 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "해당 카테고리에 영화가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
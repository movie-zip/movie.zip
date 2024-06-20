from rest_framework import serializers
from .models import Category
from movies.models import Movie

class CategoryListSerializer(serializers.ModelSerializer): # category 생성 / 리스트 조회

    class Meta:
        model = Category
        fields = ('id', 'name',)

class CategorySerializer(serializers.ModelSerializer):  # 특정 카테고리 수정, 삭제, 카테고리 detail 조회

    class MovieSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = ('id', 'title', 'poster_path')
    
    movies = MovieSerializer(read_only=True, many=True)
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('user',)


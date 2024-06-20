from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Movie, Genre, Actor, Rating

User = get_user_model()


class MovieSerializer(serializers.ModelSerializer):

    class GenreSerializer(serializers.ModelSerializer):
        class Meta:
            model = Genre
            fields = ('name',)

    class ActorSerializer(serializers.ModelSerializer):
        class Meta:
            model = Actor
            fields = ('name',)

    # class RateSerializer(serializers.ModelSerializer):
    #     class Meta:
    #         model = Rating
    #         fields = '__all__'

    genres = GenreSerializer(read_only=True, many=True)
    actors = ActorSerializer(read_only=True, many=True)
    # rate = RateSerializer(read_only=True, many=True)

    class Meta:
        model = Movie
        fields = '__all__'

# 영화 평점 등록
class RatingSerializer(serializers.ModelSerializer):

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields =('pk', 'username',)

    user = UserSerializer(read_only=True)

    class Meta:
        model = Rating
        fields= '__all__'
        read_only_fields = ('movie',)
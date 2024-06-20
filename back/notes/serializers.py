from rest_framework import serializers
from .models import Note, Comment
from movies.models import Movie

class CommentSerializer(serializers.ModelSerializer):  # comment 상세, 작성, 삭제
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('note', 'user',)

class NoteSerializer(serializers.ModelSerializer):  # note 상세, 작성

    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Note
        fields = ('id', 'user', 'movie', 'content', 'created_at', 'updated_at', 'comments',)
        read_only_fields = ('user', 'movie',)

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'poster_path',)

class FollowingNoteSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    movie = MovieSerializer(read_only=True)
    
    class Meta:
        model = Note
        fields = ('id', 'content', 'created_at', 'user', 'movie')
        read_only_fields = ('id', 'created_at', 'user')

    def get_user(self, obj):
        # default_img_url = "https://example.com/default_profile_img.png"  # 기본 이미지 URL
        return {
            "user_id": obj.user.id,
            "nickname": obj.user.nickname,
            # "profile_img_url": obj.user.profile_img_url if obj.user.profile_img_url else default_img_url
        }

        
class NoteListSerializer(serializers.ModelSerializer):  # note 목록
    movie = MovieSerializer(read_only=True)
    user = serializers.SerializerMethodField()
    class Meta:
        model = Note
        fields = ('id', 'content', 'created_at', 'movie', 'user')

    def get_user(self, obj):
        return {
            "user_id": obj.user.id,
            "nickname": obj.user.nickname,
            # "profile_img_url": obj.user.profile_img_url
        }

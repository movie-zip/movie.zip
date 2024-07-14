from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model
from movies.models import Movie
from notes.models import Note
from categories.models import Category


class CustomRegisterSerializer(RegisterSerializer):
    # 필요한 필드들을 추가합니다.
    nickname = serializers.CharField(
        max_length=30
    )
    profile_url = serializers.ImageField(
        # required=False = 이 필드는 필수 X / 기본값은 True
        required=False,
        use_url=True
    )

 # 해당 필드도 저장 시 함께 사용하도록 설정합니다.
    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            # nickname, profile_url 필드 추가
            'nickname': self.validated_data.get('nickname', ''),
            'profile_url': self.validated_data.get('profile_url', '')
        }


# nickname 필드도 추가하여, 우리만의 UserDetailsSerializer 를 작성
User = get_user_model()

class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta:
        extra_fields = []
        # see https://github.com/iMerica/dj-rest-auth/issues/181
        # UserModel.XYZ causing attribute error while importing other
        # classes from `serializers.py`. So, we need to check whether the auth model has
        # the attribute or not
        if hasattr(User, 'USERNAME_FIELD'):
            extra_fields.append(User.USERNAME_FIELD)
        # if hasattr(UserModel, 'EMAIL_FIELD'):
        #     extra_fields.append(UserModel.EMAIL_FIELD)
        # if hasattr(UserModel, 'first_name'):
        #  extra_fields.append('first_name')
        # if hasattr(UserModel, 'last_name'):
        #     extra_fields.append('last_name')
        if hasattr(User, 'nickname'):
            extra_fields.append('nickname') 
        model = User
        fields = ('pk', *extra_fields)
        read_only_fields = ('email',)


class MyMoviesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'poster_path',)

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name',)

class ProfileSerializer(serializers.ModelSerializer):
    # 닉네임, 프로필 사진
    # 내가 선정한 5가지 영화
    # 내가 가진 카테고리 리스트

    def get_my_movies(self, obj):
        # 'Category1'이라는 이름의 카테고리를 찾습니다.
        category1 = obj.categories.filter(name='Category1').first()
        if category1:
            # 해당 카테고리에 속한 모든 영화를 가져옵니다.
            movies = category1.movies.all()
            # 이 영화들을 MyMoviesSerializer를 사용하여 시리얼라이즈합니다.
            return MyMoviesSerializer(movies, many=True).data
        return None


    def get_my_categories(self, obj):
        # 사용자가 가진 모든 카테고리를 가져와서 CategoryListSerializer로 시리얼라이즈합니다.
        categories = obj.categories.all()  # 사용자의 모든 카테고리를 가져옵니다.
        return CategoryListSerializer(categories, many=True).data
    
    my_movies = serializers.SerializerMethodField('get_my_movies')
    my_categories = serializers.SerializerMethodField('get_my_categories')  # 사용자의 카테고리 리스트 정보

    class Meta:
        model = User
        fields = ('id', 'nickname', 'profile_img_url', 'my_movies', 'my_categories', 'followings', 'followers')


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'nickname', 'profile_img_url',)
from django.db import models
from django.contrib.auth.models import AbstractUser
from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings

# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=30, unique=True)
    profile_img_url = models.ImageField(
        upload_to='profile_images/', 
        blank=True, 
        null=True, 
        default='profile_img.jpg'
    )
    email = models.EmailField(null=True)
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    first_name = None
    last_name = None

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        from allauth.account.utils import user_field, user_username
        data = form.cleaned_data
        email = data.get("email")
        username = data.get("username")
        # nickname 필드를 추가
        nickname = data.get("nickname")
        user_username(user, username)
        if nickname:
            user_field(user, "nickname", nickname)
        if "password1" in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
            # Ability not to commit makes it easier to derive from
            # this adapter by adding
            user.save()
        return user



# import os
# from django.conf import settings
# from django.core.files import File
# from accounts.models import User

# # Static 폴더 경로 설정
# static_folder = os.path.join(settings.BASE_DIR, 'static', 'images')
# profile_img_path = os.path.join(static_folder, 'profile1.jpg')

# # 이미지 파일이 존재하는지 확인
# if os.path.exists(profile_img_path):
#     # 모든 유저 모델 인스턴스 순회
#     for user in User.objects.all():
#         with open(profile_img_path, 'rb') as f:
#             user.profile_img_url.save('profile1.jpg', File(f), save=True)
# else:
#     print("Image not found: profile1.jpg")


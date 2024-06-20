from django.conf import settings
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from .models import User
from categories.models import Category


# 이 시그널은 사용자가 성공적으로 회원가입을 마쳤을 때 발생
# user_signed_up 시그널을 사용하여 사용자에게 세 개의 기본 카테고리를 자동으로 부여
@receiver(user_signed_up)
def create_user_categories(sender, **kwargs):
    user = kwargs['user']   # 회원가입을 완료한 사용자 객체
    categories_names = ['Category1', 'Category2', 'Category3']
    for name in categories_names:
        Category.objects.create(user=user, name=name)

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

import json
from datetime import datetime
import random
import string
from movies.models import Movie
from django.contrib.auth.hashers import make_password

# movie.json loaddata 해놓고 실행시켜야 합니다..

# def generate_password():
#     chars = string.ascii_letters + string.digits
#     return "pbkdf2_sha256$600000$" + ''.join(random.choice(string.ascii_lowercase) for _ in range(8)) + "$" + ''.join(random.choice(chars) for _ in range(44))

def generate_password():
    # 실제 사용할 평문 비밀번호
    plain_password = '456789dd'
    # 평문 비밀번호를 해싱
    hashed_password = make_password(plain_password)
    return hashed_password


def generate_user(pk, username, nickname):
    user = {
        "model": "accounts.user",
        "pk": pk,
        "fields": {
            "password": generate_password(),
            "last_login": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "is_superuser": False,
            "username": username,
            "is_staff": False,
            "is_active": True,
            "date_joined": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "nickname": nickname,
            "profile_img_url": "",
            "email": None,
            "groups": [],
            "user_permissions": [],
            "followings": []
        }
    }
    return user

def get_random_movie_pks(count=5):
    # Movie 모델로부터 모든 movie의 pk를 조회
    all_movie_pks = Movie.objects.all().values_list('pk', flat=True)
    # 랜덤하게 5개의 movie_pk를 선택
    random_movie_pks = random.sample(list(all_movie_pks), min(len(all_movie_pks), count))
    return random_movie_pks

def generate_category(user_pk, pk, name):
    # 'get_random_movie_pks' 함수를 사용하여 랜덤으로 선택된 'movie_pk' 값
    random_movies = get_random_movie_pks()
    
    category = {
        "model": "categories.category",
        "pk": pk,
        "fields": {
            "user": user_pk,
            "name": name,
            "movies": random_movies
        }
    }
    return category

def create_dummy_data(num_users):
    users = []
    categories = []
    category_pk = 1
    for user_pk in range(1, num_users + 1):
        username = f"user{str(user_pk).zfill(4)}"
        nickname = f"유저{user_pk}"
        user = generate_user(user_pk, username, nickname)
        users.append(user)
        for i in range(1, 4):  # Generate 3 categories for each user
            category_name = f"Category{i}"
            category = generate_category(user_pk, category_pk, category_name)
            categories.append(category)
            category_pk += 1
    return users, categories

if __name__ == "__main__":
    num_users = 300  # 원하는 사용자 수
    dummy_users, dummy_categories = create_dummy_data(num_users)
    
    with open("user.json", "w", encoding="utf-8") as f:
        json.dump(dummy_users, f, ensure_ascii=False, indent=4)
        
    with open("category.json", "w", encoding="utf-8") as f:
        json.dump(dummy_categories, f, ensure_ascii=False, indent=4)

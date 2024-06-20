from django.db import models
from django.conf import settings
# from movies.models import Movie

# Create your models here.
class Category(models.Model):
    movies = models.ManyToManyField('movies.Movie', related_name='categories', blank=True)
    # blank=True 해야지 카테고리 생성 시 영화를 넣지 않더라도 에러가 안 뜸
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=30)
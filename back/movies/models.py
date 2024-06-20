from django.db import models
from django.conf import settings
import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class Actor(models.Model):
    name = models.CharField(max_length=30)
    profile_url = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.name
    
class Genre(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Movie(models.Model):
    actors = models.ManyToManyField(Actor, related_name='movies')
    genres = models.ManyToManyField(Genre, related_name='movies')
    title = models.CharField(max_length=300)
    content = models.TextField(null=True)
    release_date = models.DateField(null=True, default=datetime.date.today)
    runtime = models.IntegerField(null=True)
    rank = models.FloatField(null=True)
    poster_path = models.CharField(max_length=200, null=True)

    # def __str__(self):
    #     return self.title

class Poster(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='posters')
    img_url = models.TextField()


class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ratings')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    rate = models.IntegerField(null=True, validators=[MinValueValidator(1), MaxValueValidator(10)])
    
    def __str__(self):
        return self.user


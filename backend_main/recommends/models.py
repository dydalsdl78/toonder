from django.db import models
from django.conf import settings

from accounts.models import User 

# Create your models here.
class Genre(models.Model):
    genre_name = models.CharField(max_length=50)


class Webtoon(models.Model):
    webtoon_number = models.AutoField(primary_key=True)
    webtoon_name = models.CharField(max_length=100)
    overview = models.TextField()
    webtoon_writer = models.CharField(max_length=50)
    thumbnail_url = models.TextField()
    webtoon_score = models.FloatField()
    webtoon_link = models.TextField(default='')
    webtoon_platform = models.TextField(default='')
    serialized_day = models.TextField(default='')
    overview_morph = models.TextField()

    genres = models.ManyToManyField(Genre, related_name='webtoons')
    users_webtoon = models.ManyToManyField(User, related_name='favorites')


class Like(models.Model):
    is_like = models.BooleanField(default=False)

    users_like = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    webtoons_like = models.ForeignKey(Webtoon, on_delete=models.CASCADE, related_name='like_webtoon')

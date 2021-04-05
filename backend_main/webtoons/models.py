from django.db import models
from django.conf import settings


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
    users_webtoon = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='favorites')
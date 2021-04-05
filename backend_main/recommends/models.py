from django.db import models
from django.conf import settings

from webtoons.models import Webtoon, Genre


class Like(models.Model):
    is_like = models.BooleanField(default=False)

    users_like = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    webtoons_like = models.ForeignKey(Webtoon, on_delete=models.CASCADE, related_name='like_webtoon')

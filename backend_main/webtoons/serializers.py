from rest_framework import serializers, viewsets

from .models import Webtoon, Genre


class WebtoonSerializer(serializers.ModelSerializer):

  class Meta:
    model = Webtoon
    fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):

  class Meta:
    model = Genre
    fields = '__all__'
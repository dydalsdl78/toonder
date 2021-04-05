from rest_framework import serializers, viewsets
from .models import Webtoon


class WebtoonSerializer(serializers.ModelSerializer):

  class Meta:
    model = Webtoon
    fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):

  class Meta:
    model = Genre
    fields = '__all__'
from rest_framework import serializers
from .models import Webtoon


class WebtoonSerializer(serializers.ModelSerializer):

  class Meta:
    model = Webtoon
    fields = '__all__'

class SummarySerializer(serializers.ModelSerializer):

  class Meta:
    model = Webtoon
    fields = ('webtoon_name',
              'overview',
              'webtoon_writer',
              'thumbnail_url',
              'webtoon_score',
              'webtoon_link',
              'webtoon_platform',
              'serialized_day')
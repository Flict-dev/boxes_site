from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from reviews.models import Reviews


class ReviewSerializer(ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Reviews
        fields = '__all__'

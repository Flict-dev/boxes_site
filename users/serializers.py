from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator

from users.models import User


class UserSerializer(ModelSerializer):
    username = serializers.CharField(max_length=100,
                                     required=True,
                                     validators=[UniqueValidator(queryset=User.objects.all())]
                                     )

    class Meta:
        model = User
        fields = '__all__'

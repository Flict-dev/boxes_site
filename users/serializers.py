from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100,
                                     required=True,
                                     validators=[UniqueValidator(queryset=User.objects.all())]
                                     )

    class Meta:
        model = User
        fields = [
            'id',
            'password',
            'username',
            'email',
            'first_name',
            'last_name',
            'middle_name',
            'phone',
            'address',
        ]

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            middle_name=validated_data['middle_name'],
            phone=validated_data['phone'],
            address=validated_data['address']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

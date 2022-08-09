from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True,
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True,
    )

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'Никнейм "me" нельзя регистрировать!'
            )
        return username

    class Meta:
        model = User
        fields = '__all__'


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

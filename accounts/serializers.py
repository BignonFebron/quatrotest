from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from accounts.models import APIKeys
import secrets

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    username = serializers.CharField(
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField()

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],
             validated_data['password'])
        return user

    class Meta:
        model = User
        fields = ('id','username','email','password')

class APIKeysSerializer():
    def create(self,user_id):
        keys = APIKeys.objects.create(public_key=secrets.token_hex(64), private_key=secrets.token_hex(64),
             user_id=user_id)
        return keys
    class Meta:
        model = User
        fields = ('id','public_key','private_key')

        
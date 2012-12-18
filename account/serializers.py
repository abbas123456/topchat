from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'id')

    def save(self, save_m2m=True):
        self.object.password = make_password(self.object.password)
        super(UserSerializer, self).save(save_m2m)


class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from client.models import RoomAdministrator


class RoomAdministratorSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomAdministrator
        fields = ('room',)


class UserSerializer(serializers.ModelSerializer):

    administrated_rooms = RoomAdministratorSerializer(source='roomadministrator_set')

    class Meta:
        model = User
        fields = ('username', 'password', 'id', 'administrated_rooms')

    def save(self, save_m2m=True):
        self.object.password = make_password(self.object.password)
        super(UserSerializer, self).save(save_m2m)


class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

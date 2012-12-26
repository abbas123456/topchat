from client.models import Room, RoomBannedUser
from rest_framework import serializers


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ('name', 'id', 'is_active')


class BannedUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomBannedUser
        fields = ('banned_user', 'room')
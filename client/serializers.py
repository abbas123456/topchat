from client.models import Room, RoomAdministrator
from rest_framework import serializers


class RoomAdministratorSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomAdministrator
        fields = ('administrator',)


class RoomSerializer(serializers.ModelSerializer):
    administrators = RoomAdministratorSerializer(source='roomadministrator_set')

    class Meta:
        model = Room
        fields = ('name', 'id', 'administrators')

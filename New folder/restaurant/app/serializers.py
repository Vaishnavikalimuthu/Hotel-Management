from app.models import Room
from rest_framework import serializers

from .models import Room

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['number', 'beds', 'capacity']
from rest_framework import serializers
from .models import Users


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('email', 'verified')


class InputSerializer(serializers.Serializer):
    INN = serializers.CharField()
    UKEP = serializers.CharField()
    MCHD = serializers.CharField()
    email = serializers.EmailField()

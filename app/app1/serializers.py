from rest_framework import serializers
from .models import Users


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('email', 'verified')

class InputSerializer(serializers.Serializer):
    first_input = serializers.CharField()
    second_input = serializers.CharField()
    email = serializers.EmailField()
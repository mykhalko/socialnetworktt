from rest_framework.serializers import ModelSerializer

from .models import User


class UserCreatingSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserRetrievingSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = 'is_staff', 'password'

from rest_framework import serializers
from main.models import CustomUser, Card
from django.contrib.auth import authenticate

# Рег / Авторизация
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Неверные учетные данные")
        return user

# Пользователь
class UserSerializer(serializers.ModelSerializer):
    days_on_site = serializers.ReadOnlyField()

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'phone', 'days_on_site', 'role', 'is_active', 'is_staff')

# Объявления
class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'title', 'image', 'created_at', 'user']
        read_only_fields = ['id', 'created_at', 'user']

# Доп информация о пользователе
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('user_type', 'first_name', 'last_name', 'middle_name',
                  'company_name', 'phone', 'profile_image')

        
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from . custom_auth import CustomAuthBackend
from . models import RefreshTokenModels

User = get_user_model()


class CustomUserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['phone_number', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

        refresh = RefreshToken.for_user(user)
        RefreshTokenModels.objects.create(user=user, token=str(refresh))
        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        refresh = RefreshToken.for_user(instance)
        representation['access'] = str(refresh.access_token)
        representation['refresh'] = str(refresh)
        return representation


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'login'
    login = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        login = attrs.get("login")
        password = attrs.get("password")

        if login and password:
            user = self.authenticate_user(login, password)
            if user:
                refresh = RefreshToken.for_user(user)
                refresh_token_instance, created = RefreshTokenModels.objects.get_or_create(
                    user=user,
                    defaults={'token': str(refresh)}
                )
                if not created:
                    refresh_token_instance.token = str(refresh)
                    refresh_token_instance.save()

                data = {
                    'token': {
                        'access': str(refresh.access_token),
                    },
                    'user': {
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'phone_number': user.phone_number,
                        'id': user.id,
                    }
                }

                return data
            else:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'login' and 'password'.")

    def authenticate_user(self, login, password):
        user = CustomAuthBackend().authenticate(request=None, login=login, password=password)
        return user

class CustomUserUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'first_name', 'last_name']

    def update(self, instance, validated_data):
        phone_number = validated_data.get('phone_number', instance.phone_number)
        if phone_number == '':
            return None

        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance

class PasswordChangeSerializer(serializers.Serializer):
    # old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    new_password_confirm = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError("New passwords do not match.")
        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
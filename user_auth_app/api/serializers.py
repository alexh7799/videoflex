from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string



class RegistrationSerializer(serializers.ModelSerializer):
    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [ 'email', 'password', 'confirmed_password']
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'email': {
                'required': True
            }
        }

    def validate(self, data):
        if data['password'] != data['confirmed_password']:
            raise serializers.ValidationError({'error': 'passwords do not match'})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'error': 'This email is already in use'})
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirmed_password')
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False
        )
        activation_token = get_random_string(148)
        user.activation_token = activation_token
        user.save()
        return {
            'user': user,
            'token': activation_token
        }
        


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            self.fields.pop('username')

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                raise serializers.ValidationError('User account is inactive.')
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid email or password.')
        if not email or not password:
            raise serializers.ValidationError('Email and password are required.')
        if not user.check_password(password):
            raise serializers.ValidationError('Invalid email or password.')
        data = super().validate({"username": user.username, "password": password})
        return data
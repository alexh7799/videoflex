from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string



class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'email': {
                'required': True
            }
        }

    def validate_repeated_password(self, value):
        password = self.initial_data.get('password')
        if password and value and password != value:
            raise serializers.ValidationError('Passwords do not match')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False
        )
        
        activation_token = get_random_string(2048)
        user.activation_token = activation_token
        user.save()
        return {
            'user': {
                'id': user.id,
                'email': user.email
            },
            'token': activation_token
        }

    # def save(self):
    #     pw = self.validated_data['password']

    #     account = User(email=self.validated_data['email'], username=self.validated_data['email'])
    #     account.set_password(pw)
    #     account.save()
    #     return account
    
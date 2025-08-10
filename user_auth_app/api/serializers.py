from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string



class RegistrationSerializer(serializers.ModelSerializer):
    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirmed_password']
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
            raise serializers.ValidationError({'error': 'passwords do not match'}, status=400)
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'error': 'This email is already in use'}, status=400)
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirmed_password')
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
    
class TokenObtainPairSerializerWithCookie(TokenObtainPairSerializer):
    pass
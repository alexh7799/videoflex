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
        """
        Validates the given data.

        Checks if the passwords and email provided in the data match and if the email is already in use.
        If there are any errors, it raises a serializers.ValidationError. Otherwise, it returns the validated data.

        Args:
            data (dict): The data to be validated. It should have the following keys:
                - 'password': The password provided by the user.
                - 'confirmed_password': The confirmed password provided by the user.
                - 'email': The email provided by the user.

        Raises:
            serializers.ValidationError: If the passwords do not match or if the email is already in use.

        Returns:
            dict: The validated data.
        """
        if data['password'] != data['confirmed_password']:
            raise serializers.ValidationError({'error': 'passwords do not match'})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'error': 'This email is already in use'})
        return data
    
    def create(self, validated_data):
        """
        Creates a new user with the given validated data.

        Args:
            validated_data (dict): A dictionary containing the validated data for the user.
                It should have the following keys:
                    - 'email': The email of the user.
                    - 'password': The password of the user.
        
        Returns:
            dict: A dictionary containing the user object and the activation token.
                It has the following keys:
                    - 'user': The created user object.
                    - 'token': The activation token for the user.
        """
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
        """
        Initializes the CustomTokenObtainPairSerializer.

        This method overrides the __init__ method of the parent class
        (TokenObtainPairSerializer) to remove the 'username' field from the
        serializer fields.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None
        """
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            self.fields.pop('username')

    def validate(self, attrs):
        """
        Validates the given attributes.

        This method validates the email and password provided in the attributes.
        It checks if the user with the given email exists and if the user's account is active.
        If the email or password is missing, it raises a serializers.ValidationError.
        If the password is incorrect, it raises a serializers.ValidationError.
        If all the checks pass, it returns the validated data.

        Args:
            attrs (dict): A dictionary containing the email and password.

        Returns:
            dict: The validated data.

        Raises:
            serializers.ValidationError: If the email or password is missing
                                        or if the password is incorrect.
        """
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
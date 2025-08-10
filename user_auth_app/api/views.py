import django_rq
import base64
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .serializers import RegistrationSerializer
from ..tasks import send_activation_email, send_password_reset_email



class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Post method to handle registration request.
        Args:
            request (Request): The request object
        Returns:
            Response: A response object with the registered user's information if successful, otherwise a response object with the errors.
        """
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            saved_account = serializer.save()
            queue = django_rq.get_queue('default', autocommit=True)
            queue.enqueue(send_activation_email, saved_account, request)
            data = { 'username': saved_account.username, 'email': saved_account.email, 'user_id': saved_account.pk }
            return Response(data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CookieLoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        """
        Post method to handle login request and set refresh and access tokens to cookies.
        Args:
            request (Request): The request object
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        Returns:
            Response: A response object with the access token and refresh token as cookies.
        """
        serializer = self.serializer_class(data=request.data)
        response = super().post(request, *args, **kwargs)
        refresh_token = response.data.get('refresh')
        access_token = response.data.get('access')
        if refresh_token:
            response.set_cookie('refresh_token', value=refresh_token, secure=True, httponly=True, samesite='Lax')
        else:
            return Response(serializer.errors, content_type='application/json', status=status.HTTP_400_BAD_REQUEST)
        if access_token:
            response.set_cookie('access_token', value=access_token, secure=True, httponly=True, samesite='Lax')
        else:
            return Response(serializer.errors, content_type='application/json', status=status.HTTP_400_BAD_REQUEST)
        response.data = {'message': 'Login successful'}
        return response


class ActivationView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, uidb64, token):
        """
        Handles the account activation process using a token.
        Args:
            request: The HTTP request object.
            uidb64: Base64 encoded user ID.
            token: Activation token.
        Returns:
            Response object indicating the success or failure of the activation process.
            - On success: Returns a 200 OK status with a success message.
            - On failure: Returns a 400 Bad Request status with an error message.
        """
        try:
            uid = base64.urlsafe_b64decode(uidb64.encode()).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, base64.binascii.Error):
            return Response({'message': 'Activation failed.'}, status=status.HTTP_400_BAD_REQUEST)
        if hasattr(user, 'activation_token') and user.activation_token == token and not user.is_active:
            user.is_active = True
            user.activation_token = ''
            user.save()
            return Response({'message': 'Account successfully activated.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Activation failed.'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Handles the logout process by blacklisting the refresh token and deleting access and refresh
        tokens from the cookies.
        Args:
            request (Request): The request object with cookies containing the refresh token.
        Returns:
            Response: A response object indicating the success or failure of the logout process.
            - On success: Returns a 200 OK status with a success message and deletes cookies.
            - On failure: Returns a 400 Bad Request status with an error message if the refresh token
            is missing or invalid.
        """
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'detail': 'Refresh token missing.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return Response({'detail': 'Invalid refresh token.'}, status=status.HTTP_400_BAD_REQUEST)
        response = Response({'detail': 'Logout successful! All tokens will be deleted. Refresh token is now invalid.'}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response


class TokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handles the refresh token request by returning a new access token and updating the access_token
        cookie.
        Args:
            request (Request): The request object with the refresh_token cookie.
        Returns:
            Response: A response object with the new access token and a success message.
            - On success: Returns a 200 OK status with a new access token and updates the access_token cookie.
            - On failure: Returns a 400 Bad Request status with an error message if the refresh token
            is missing or invalid.
        """
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'detail': 'Refresh token missing.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            access_token = str(token.access_token)
        except TokenError:
            return Response({'detail': 'Invalid refresh token.'}, status=status.HTTP_401_UNAUTHORIZED)
        response = Response({'detail': 'Token refreshed', 'access': access_token}, status=status.HTTP_200_OK)
        response.set_cookie('access_token', value=access_token, secure=True, httponly=True, samesite='Lax')
        return response


class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handles the password reset request by sending an email to the user with a link to
        reset their password.
        Args:
            request (Request): The request object with the email to reset the password for.
        Returns:
            Response: A response object with a success message indicating that an email has been sent to reset the password.
            - On success: Returns a 200 OK status with a success message.
            - On failure: Returns a 400 Bad Request status with an error message if the email is missing or invalid.
        """
        email = request.data.get('email')
        if not email:
            return Response({'detail': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            queue = django_rq.get_queue('default', autocommit=True)
            userExists = queue.enqueue(send_password_reset_email, email, request) 
        except userExists.DoesNotExist:
            pass
        return Response({'detail': 'An email has been sent to reset your password.'}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        """
        Handles the password reset confirmation process.
        Args:
            request (Request): The HTTP request object containing the new password and confirmation password.
            uidb64 (str): Base64 encoded user ID.
            token (str): Password reset token.
        Returns:
            Response: A response object indicating the success or failure of the password reset process.
            - On success: Returns a 200 OK status with a success message.
            - On failure: Returns a 400 Bad Request status with an error message if the passwords do not match,
            required fields are missing, the user ID is invalid, or the token is invalid or expired.
        """
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')
        if not new_password or not confirm_password:
            return Response({'detail': 'Both password fields are required.'}, status=status.HTTP_400_BAD_REQUEST)
        if new_password != confirm_password:
            return Response({'detail': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            uid = base64.urlsafe_b64decode(uidb64.encode()).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, base64.binascii.Error):
            return Response({'detail': 'Invalid link.'}, status=status.HTTP_400_BAD_REQUEST)
        if not default_token_generator.check_token(user, token):
            return Response({'detail': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        return Response({'detail': 'Your Password has been successfully reset.'}, status=status.HTTP_200_OK)
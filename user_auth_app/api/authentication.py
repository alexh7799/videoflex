from rest_framework_simplejwt.authentication import JWTAuthentication

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        """
        Authenticates a user based on the 'access_token' cookie in the request.
        
        Args:
            request (HttpRequest): The HTTP request object.
            
        Returns:
            tuple: A tuple containing the authenticated user and the validated token.
                If the 'access_token' cookie is missing or invalid, returns None.
        """
        token = request.COOKIES.get('access_token')
        if not token:
            return None
        validated_token = self.get_validated_token(token)
        return self.get_user(validated_token), validated_token
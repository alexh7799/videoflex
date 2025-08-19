from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.tokens import UntypedToken
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

class HasValidCookieJWT(BasePermission):
    """
    Erlaubt Zugriff nur, wenn ein gültiger JWT im 'access_token'-Cookie vorhanden ist.
    """
    def has_permission(self, request, view):
        token = request.COOKIES.get('access_token')
        if not token:
            return False
        try:
            UntypedToken(token)
            return True
        except (InvalidToken, TokenError):
            return False


from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

class UserAuthTests(APITestCase):
    def setUp(self):
        """
        Sets up a test user for the tests in this class. The user is created as inactive.

        This user is used in the tests to verify that the authentication views are working correctly.
        """
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword',
            is_active=False
        )

    def test_registration(self):
        """
        Tests the registration endpoint.

        Creates a new user using the registration endpoint and verifies that the response has a 201 status code and that the user exists in the database.
        """
        url = reverse('register')
        data = {
            'email': 'newuser@example.com',
            'password': 'securepassword',
            'repeated_password': 'securepassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_activation(self):
        """
        Tests the account activation view.

        Creates an inactive user, then uses the activation view to activate their account.
        and that the user's is_active field is now True.
        """
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        url = reverse('activate', args=[uid, token])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_login(self):
        """
        Tests the login endpoint.

        Creates an active user, then authenticates that user and makes a POST request to the login endpoint.
        Verifies that the response has a 200 status code and includes the access and refresh tokens.
        """
        self.user.is_active = True
        self.user.save()
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_logout(self):
        """
        Tests the logout endpoint.

        Creates an active user, then authenticates that user and makes a POST request to the logout endpoint.
        Verifies that the response has a 200 status code and a success message, and that the refresh token is now invalid.
        """
        self.user.is_active = True
        self.user.save()
        url = reverse('logout')
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['detail'], 'Logout successfull! All tokens will be deleted. Refresh token is now invalid.')

    def test_password_reset(self):
        """
        Tests the password reset endpoint.

        Creates an active user, then makes a POST request to the password reset endpoint with the user's email.
        Verifies that the response has a 200 status code and a success message.
        """
        url = reverse('password_reset')
        data = {'email': 'testuser@example.com'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['detail'], 'An email has been sent to reset your password.')

    def test_password_reset_confirm(self):
        """
        Tests the password reset confirmation view.

        Creates an active user, then uses the password reset confirmation view to change their password.
        and that the user's password has been changed to the new value.
        """
        self.user.is_active = True
        self.user.save()
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        url = reverse('password_confirm', args=[uid, token])
        data = {
            'new_password': 'newsecurepassword',
            'confirm_password': 'newsecurepassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['detail'], 'Your Password has been successfully reset.')
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newsecurepassword'))

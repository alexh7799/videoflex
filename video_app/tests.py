from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Video
import os

class VideoAppTests(APITestCase):
    def setUp(self):
        """
        Set up test data.
        Create a test user and a test video, as well as the URLs for the video list,
        manifest, and segment views.
        """
        self.user = User.objects.create_user(username='tester', password='testpass')
        self.video = Video.objects.create(
            title='Test Movie',
            description='Test Description',
            thumbnail_url='http://example.com/image.jpg',
            category='Drama'
        )
        self.list_url = reverse('video-list')
        self.manifest_url = reverse('video-manifest', args=[self.video.id, '720p'])
        self.segment_url = reverse('video-segment', args=[self.video.id, '720p', 'index0.ts'])

    def authenticate(self):
        """
        Authenticate the test client with the test user.
        This is a helper method used by the other tests in this class to
        authenticate the test client with the test user before making requests
        to the video app views.
        :return: None
        """
        self.client.force_authenticate(user=self.user)

    def test_video_list_requires_auth(self):
        """
        Tests that authentication is required to access the video list endpoint.
        Makes a GET request to the video list URL without authenticating.
        Verifies that the response status code is 401 Unauthorized.
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_video_list_success(self):
        """
        Tests successful retrieval of the video list.
        Authenticates the test client and makes a GET request to the video list endpoint.
        Verifies that the response status code is 200 OK, the response contains one video,
        and the video's title matches 'Test Movie'.
        """
        self.authenticate()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Movie')

    def test_manifest_not_found(self):
        """
        Tests that a 404 error is returned when the manifest URL is accessed without
        the manifest file existing. Authenticates the test client and makes a GET request
        to the manifest URL. Verifies that the response status code is 404 Not Found.
        """
        self.authenticate()
        response = self.client.get(self.manifest_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_segment_not_found(self):
        """
        Tests that a 404 error is returned when the segment URL is accessed without
        the segment file existing. Authenticates the test client and makes a GET request
        to the segment URL. Verifies that the response status code is 404 Not Found.
        """
        self.authenticate()
        response = self.client.get(self.segment_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
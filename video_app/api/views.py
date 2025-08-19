import os
from django.http import FileResponse, Http404
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from ..models import Video
from .serializers import VideoSerializer
from user_auth_app.api.authentication import CookieJWTAuthentication
from user_auth_app.api.permissions import HasValidCookieJWT


class VideoListView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [HasValidCookieJWT]

    def get(self, request):  
        """
        Get a list of all videos.
        Args:
            request (HttpRequest): The HTTP request object. 
        Returns:
            Response: A response containing a list of all videos serialized as JSON.
        """
        try:
            videos = Video.objects.all()
        except Video.DoesNotExist:
            raise Http404("Videos not found.")
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class VideoManifestView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [HasValidCookieJWT]

    def get(self, request, movie_id, resolution):
        """
        Get the manifest file for a video.
        Args:
            request (HttpRequest): The HTTP request object.
            movie_id (int): The ID of the video.
            resolution (str): The resolution of the video.   
        Returns:
            FileResponse: The manifest file for the video.
        Raises:
            Http404: If the manifest file is not found.
        """
        try:
            video = Video.objects.get(pk=movie_id)
        except Video.DoesNotExist:
            raise Http404("Video not found.")
        manifest_path = os.path.join(
            settings.MEDIA_ROOT, 'uploads', 'videos', 'hls', resolution, str(movie_id), 'index.m3u8'
        )
        if not os.path.exists(manifest_path):
            raise Http404("Video not found.")
        return FileResponse(open(manifest_path, 'rb'), content_type='application/vnd.apple.mpegurl')
    
    
class VideoSegmentView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [HasValidCookieJWT]

    def get(self, request, movie_id, resolution, segment):
        """
        Get a video segment.
        Args:
            request (HttpRequest): The HTTP request object.
            movie_id (int): The ID of the video.
            resolution (str): The resolution of the video.
            segment (str): The name of the segment file.  
        Returns:
            FileResponse: The video segment file. 
        Raises:
            Http404: If the video or segment file is not found.
        """
        try:
            video = Video.objects.get(pk=movie_id)
        except Video.DoesNotExist:
            raise Http404("Video not found.")
        segment_path = os.path.join(
            settings.MEDIA_ROOT, 'uploads', 'videos', 'hls', resolution, str(movie_id), segment
        )
        if not os.path.exists(segment_path):
            raise Http404("Video not found.")
        return FileResponse(open(segment_path, 'rb'), content_type='video/MP2T')
import os
from django.http import FileResponse, Http404
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import Video
from .serializers import VideoSerializer
from user_auth_app.api.authentication import CookieJWTAuthentication

class VideoListView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class VideoManifestView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    # def get(self, request, movie_id, resolution):
    #     try:
    #         video = Video.objects.get(pk=movie_id)
    #     except Video.DoesNotExist:
    #         raise Http404("Video not found.")
    #     m3u8_field = f"{resolution}"
    #     m3u8_file = getattr(video, m3u8_field, None)
    #     if not m3u8_file or not m3u8_file.name:
    #         return Response({"detail": "Manifest not found."}, status=status.HTTP_404_NOT_FOUND)
    #     response = FileResponse(m3u8_file.open(), content_type='application/vnd.apple.mpegurl')
    #     response['Content-Disposition'] = 'inline; filename="index.m3u8"'
    #     return response
    
    def get(self, request, movie_id, resolution):
        manifest_path = os.path.join(
            settings.MEDIA_ROOT, 'uploads', 'videos', 'hls', resolution, str(movie_id), 'index.m3u8'
        )
        if not os.path.exists(manifest_path):
            raise Http404("Manifest not found")
        return FileResponse(open(manifest_path, 'rb'), content_type='application/vnd.apple.mpegurl')
    
    
class VideoSegmentView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, movie_id, resolution, segment):
        try:
            video = Video.objects.get(pk=movie_id)
        except Video.DoesNotExist:
            raise Http404("Video not found.")
        segment_path = os.path.join(
            settings.MEDIA_ROOT, 'uploads', 'videos', 'hls', resolution, str(movie_id), segment
        )
        if not os.path.exists(segment_path):
            raise Http404("Segment not found.")
        return FileResponse(open(segment_path, 'rb'), content_type='video/MP2T')
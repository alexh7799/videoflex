from rest_framework import serializers
from ..models import Video
import os

class VideoSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Video
        fields = ['id', 'created_at', 'title', 'description', 'thumbnail_url', 'category']

    def get_thumbnail_url(self, obj):   
        """
        Returns the URL of the thumbnail of the video object.
        Args:
            obj (Video): The video object.
        Returns:
            str: The URL of the thumbnail, or an empty string if the thumbnail is not set.
        """
        domain = os.environ.get('DOMAIN', 'http://127.0.0.1:8000')
        if obj.thumbnail and hasattr(obj.thumbnail, 'url'):
            return f'{domain}{obj.thumbnail.url}'
        return ''
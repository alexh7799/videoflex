from rest_framework import serializers
from ..models import Video

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
        request = self.context.get('request')
        if obj.thumbnail and hasattr(obj.thumbnail, 'url'):
            if request:
                return request.build_absolute_uri(obj.thumbnail.url)
            return f'http://127.0.0.1:8000{obj.thumbnail.url}'
        return ''
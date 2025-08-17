from django.db import models
from .tasks import hls_480p_upload_to, hls_720p_upload_to, hls_1080p_upload_to, thumbnail_upload_to

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to=thumbnail_upload_to, blank=True, null=True)
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    m3u8_480p = models.FileField(upload_to=hls_480p_upload_to, null=True, blank=True)
    m3u8_720p = models.FileField(upload_to=hls_720p_upload_to, null=True, blank=True)
    m3u8_1080p = models.FileField(upload_to=hls_1080p_upload_to, null=True, blank=True)

    def __str__(self):
        return self.title

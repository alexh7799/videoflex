from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail_url = models.URLField()
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    m3u8_480p = models.FileField(upload_to='hls/480p/', null=True, blank=True)
    m3u8_720p = models.FileField(upload_to='hls/720p/', null=True, blank=True)
    m3u8_1080p = models.FileField(upload_to='hls/1080p/', null=True, blank=True)

    def __str__(self):
        return self.title

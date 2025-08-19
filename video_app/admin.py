from django.contrib import admin
from .models import Video

class VideoAdmin(admin.ModelAdmin):
    exclude = ['m3u8_480p', 'm3u8_720p', 'm3u8_1080p', 'thumbnail']
    

admin.site.register(Video, VideoAdmin)

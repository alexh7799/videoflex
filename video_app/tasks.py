def hls_480p_upload_to(instance, filename):
    return f'uploads/videos/hls/480p/{instance.id}/{filename}'

def hls_720p_upload_to(instance, filename):
    return f'uploads/videos/hls/720p/{instance.id}/{filename}'

def hls_1080p_upload_to(instance, filename):
    return f'uploads/videos/hls/1080p/{instance.id}/{filename}'

def thumbnail_upload_to(instance, filename):
    return f'uploads/videos/thumbnails/{instance.id}/{filename}'
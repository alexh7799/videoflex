def hls_480p_upload_to(instance, filename):
    """
    Uploads a HLS 480p video file.

    Args:
        instance (Video): The video instance.
        filename (str): The name of the file being uploaded.

    Returns:
        str: The full path where the file will be stored.
    """
    return f'uploads/videos/hls/480p/{instance.id}/{filename}'

def hls_720p_upload_to(instance, filename):
    """
    Uploads a HLS 720p video file.

    Args:
        instance (Video): The video instance.
        filename (str): The name of the file being uploaded.

    Returns:
        str: The path for the uploaded HLS 720p video file.
    """
    return f'uploads/videos/hls/720p/{instance.id}/{filename}'

def hls_1080p_upload_to(instance, filename):
    """
    Uploads a HLS 1080p video file.

    Args:
        instance (Video): The video instance.
        filename (str): The name of the file being uploaded.

    Returns:
        str: The full path where the file will be stored.
    """
    return f'uploads/videos/hls/1080p/{instance.id}/{filename}'

def thumbnail_upload_to(instance, filename):
    """
    Uploads a thumbnail image for a video.

    Args:
        instance (Video): The video instance.
        filename (str): The name of the file being uploaded.

    Returns:
        str: The path for the uploaded thumbnail image.
    """
    return f'uploads/videos/thumbnails/{instance.id}/{filename}'

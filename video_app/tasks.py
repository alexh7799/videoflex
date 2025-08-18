import os
import subprocess
import shutil
import io
from django.conf import settings
from django.core.files.base import ContentFile
from moviepy import VideoFileClip
from PIL import Image
from .models import Video



def convert480p(source, video_id):
    """
    Convert a video file to HLS 480p format and save the generated m3u8 file.

    Args:
        source (str): The path to the video file.
        video_id (int): The ID of the video.

    Returns:
        None
    """
    target_dir = os.path.join(settings.MEDIA_ROOT, 'uploads', 'videos', 'hls', '480p', str(video_id))
    os.makedirs(target_dir, exist_ok=True)
    m3u8_file = os.path.join(target_dir, 'index.m3u8')
    cmd = (
        f'ffmpeg -i "{source}" -profile:v baseline -level 3.0 -s 854x480 -start_number 0 '
        f'-hls_time 10 -hls_list_size 0 -f hls "{m3u8_file}"'
    )
    subprocess.run(cmd, shell=True, capture_output=True)
    video = Video.objects.get(pk=video_id)
    video.m3u8_480p.save(f'index.m3u8', ContentFile(open(m3u8_file, 'rb').read()), save=True)


def convert720p(source, video_id): 
    """
    Convert a video file to HLS 720p format and save the generated m3u8 file.
    Args:
        source (str): The path to the video file.
        video_id (int): The ID of the video.
    Returns:
        None
    """
    target_dir = os.path.join(settings.MEDIA_ROOT, 'uploads', 'videos', 'hls', '720p', str(video_id))
    os.makedirs(target_dir, exist_ok=True)
    m3u8_file = os.path.join(target_dir, 'index.m3u8')
    cmd = (
        f'ffmpeg -i "{source}" -profile:v baseline -level 3.0 -s 1280x720 -start_number 0 '
        f'-hls_time 10 -hls_list_size 0 -f hls "{m3u8_file}"'
    )
    subprocess.run(cmd, shell=True, capture_output=True)
    video = Video.objects.get(pk=video_id)
    video.m3u8_720p.save(f'index.m3u8', ContentFile(open(m3u8_file, 'rb').read()), save=True)


def convert1080p(source, video_id):
    """
    Convert a video file to HLS 1080p format and save the generated m3u8 file.
    Args:
        source (str): The path to the video file.
        video_id (int): The ID of the video.
    Returns:
        None
    """
    target_dir = os.path.join(settings.MEDIA_ROOT, 'uploads', 'videos', 'hls', '1080p', str(video_id))
    os.makedirs(target_dir, exist_ok=True)
    m3u8_file = os.path.join(target_dir, 'index.m3u8')
    cmd = (
        f'ffmpeg -i "{source}" -profile:v baseline -level 3.0 -s 1920x1080 -start_number 0 '
        f'-hls_time 10 -hls_list_size 0 -f hls "{m3u8_file}"'
    )
    subprocess.run(cmd, shell=True, capture_output=True)
    video = Video.objects.get(pk=video_id)
    video.m3u8_1080p.save(f'index.m3u8', ContentFile(open(m3u8_file, 'rb').read()), save=True)


def generate_thumbnail(source, video_id):
    """
    Generate a thumbnail for a video file and save it to the database.
    Args:
        source (str): The path to the video file.
        video_id (int): The ID of the video. 
    Returns:
        None
    """
    video = Video.objects.get(pk=video_id)
    clip = VideoFileClip(source)
    frame = clip.get_frame(1)
    image = Image.fromarray(frame)
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    thumbnail_name = f'{video_id}_thumb.png'
    video.thumbnail.save(thumbnail_name, ContentFile(buffer.getvalue()), save=True)
    
def delete_video_directory(instance):
    """
    Delete the directory associated with a Video instance.
    Args:
        instance (Video): The Video instance whose directory is to be deleted.
    """
    base_dir = os.path.join('media', 'uploads', 'videos', 'hls')
    for res in ['480p', '720p', '1080p']:
        folder = os.path.join(base_dir, res, str(instance.id))
        if os.path.exists(folder):
            shutil.rmtree(folder)
    thumb_folder = os.path.join('media', 'uploads', 'videos', 'thumbnails', str(instance.id))
    if os.path.exists(thumb_folder):
        shutil.rmtree(thumb_folder)
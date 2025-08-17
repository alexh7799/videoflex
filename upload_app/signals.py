import os
import shutil
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .models import FileUpload
from video_app.models import Video
from .tasks import convert480p, convert720p, convert1080p, generate_thumbnail
import django_rq


@receiver(post_save, sender=FileUpload)
def video_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for post-save actions on Video instances.
    """
    if created and instance.file:
        video = Video.objects.create(
            title=instance.title,
            description=instance.description,
            category=instance.category
        )
        queue = django_rq.get_queue('default', autocommit=True)
        if instance.file and hasattr(instance.file, 'path'):
            queue.enqueue(convert480p, instance.file.path, video.pk)
            queue.enqueue(convert720p, instance.file.path, video.pk)
            queue.enqueue(convert1080p, instance.file.path, video.pk)
            queue.enqueue(generate_thumbnail, instance.file.path, video.pk)
    else:
        pass

@receiver(post_delete, sender=FileUpload)
def video_post_delete(sender, instance, **kwargs):
    """
    Signal handler for post-delete actions on FileUpload instances.
    Löscht das Originalvideo und alle konvertierten Formate (480p, 720p, 1080p).
    """
    if instance.file and os.path.isfile(instance.file.path):
        os.remove(instance.file.path)
    base_name = os.path.splitext(os.path.basename(instance.file.name))[0]
    for res in ['480p', '720p', '1080p']:
        hls_dir = os.path.join(os.path.dirname(instance.file.path), '..', 'hls', res, base_name)
        hls_dir = os.path.abspath(hls_dir)
        if os.path.isdir(hls_dir):
            for f in os.listdir(hls_dir):
                file_path = os.path.join(hls_dir, f)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            os.rmdir(hls_dir)
            
@receiver(post_delete, sender=Video)
def delete_video_files_and_folder(sender, instance, **kwargs):
    if instance.thumbnail:
        instance.thumbnail.delete(save=False)
    if instance.m3u8_480p:
        instance.m3u8_480p.delete(save=False)
    if instance.m3u8_720p:
        instance.m3u8_720p.delete(save=False)
    if instance.m3u8_1080p:
        instance.m3u8_1080p.delete(save=False)
    base_dir = os.path.join('media', 'uploads', 'videos', 'hls')
    for res in ['480p', '720p', '1080p']:
        folder = os.path.join(base_dir, res, str(instance.id))
        if os.path.exists(folder):
            shutil.rmtree(folder)
    thumb_folder = os.path.join('media', 'uploads', 'videos', 'thumbnails', str(instance.id))
    if os.path.exists(thumb_folder):
        shutil.rmtree(thumb_folder)
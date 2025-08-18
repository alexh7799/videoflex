import os
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .models import Video
from video_app.models import Video
from .tasks import convert480p, convert720p, convert1080p, generate_thumbnail, delete_video_directory
import django_rq


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for post-save actions on Video instances.
    """
    if created and instance.file:
        queue = django_rq.get_queue('default', autocommit=True)
        if instance.file and hasattr(instance.file, 'path'):
            queue.enqueue(convert480p, instance.file.path, instance.pk)
            queue.enqueue(convert720p, instance.file.path, instance.pk)
            queue.enqueue(convert1080p, instance.file.path, instance.pk)
            queue.enqueue(generate_thumbnail, instance.file.path, instance.pk)
    else:
        pass


            
@receiver(post_delete, sender=Video)
def delete_video_files_and_folder(sender, instance, **kwargs):
    """
    Delete all files and folders associated with a Video instance upon deletion.
    
    Args:
        sender (Video): The sender model.
        instance (Video): The deleted Video instance.
        **kwargs: Additional keyword arguments.
    """
    if instance.file and os.path.isfile(instance.file.path):
        os.remove(instance.file.path)
    if instance.thumbnail:
        instance.thumbnail.delete(save=False)
    if instance.m3u8_480p:
        instance.m3u8_480p.delete(save=False)
    if instance.m3u8_720p:
        instance.m3u8_720p.delete(save=False)
    if instance.m3u8_1080p:
        instance.m3u8_1080p.delete(save=False)
    delete_video_directory(instance)
    

import os
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .models import FileUpload
from .tasks import convert480p, convert720p, convert1080p
import django_rq


@receiver(post_save, sender=FileUpload)
def video_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for post-save actions on Video instances.
    """
    if created:
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(convert480p, instance.file.path)
        queue.enqueue(convert720p, instance.file.path)
        queue.enqueue(convert1080p, instance.file.path)
    else:
        # Perform actions after a Video instance is updated
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
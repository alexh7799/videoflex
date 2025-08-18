from django.apps import AppConfig


class VideoAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'video_app'
    
    def ready(self):
        """
        Import the signals module after the app is ready.
        """
        from . import signals

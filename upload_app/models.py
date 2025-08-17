from django.db import models

class FileUpload(models.Model):
    title = models.CharField(max_length=255, default="")
    description = models.TextField(blank=True, default="")
    category = models.CharField(max_length=100, blank=True, default="")
    file = models.FileField(upload_to='uploads/videos/original/', blank=True, null=True, default="")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    


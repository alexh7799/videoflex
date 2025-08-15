from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class UserProfile(models.Model):
    """_summary_
    UserProfile is a model that extends the User model to include additional
    information about the user.
    Returns:
        _type_: _description_
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activation_token = models.CharField(max_length=2048, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

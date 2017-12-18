"""Models for user profile."""
from django.db import models
from django.contrib.auth.models import User


class EmotionProfile(models.Model):
    """The imager profile model."""

    objects = models.Manager
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='profile')

    def __str__(self):
        """Print function returns this."""
        return self.user.username

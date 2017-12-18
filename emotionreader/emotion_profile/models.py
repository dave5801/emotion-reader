"""Models for user profile."""
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver


class EmotionProfile(models.Model):
    """The imager profile model."""

    objects = models.Manager
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='profile')

    def __str__(self):
        """Print function returns this."""
        return self.user.username


@receiver(models.signals.post_save, sender=User)
def create_profile(sender, **kwargs):
    """Create the profile when a user is created."""
    if kwargs['created']:
        profile = EmotionProfile(user=kwargs['instance'])
        profile.save()

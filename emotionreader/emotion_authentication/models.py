from django.db import models
from django.dispatch import receiver
from emotion_profile.models import User
from emotion_authentication.face_verification import FaceVerification

# Create your models here.
class FaceVerificationManager(models.Model, FaceVerification):
    objects = models.Manager
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='faces')
    auth_face = models.ImageField(upload_to='documents/%Y/%m/%d',
                              blank=True,
                              null=True)
    def __str__(self):
        """Print function returns this."""
        return self.user.username


@receiver(models.signals.post_save, sender=User)
def create_face_verification_object(sender, **kwargs):
    """Create the profile when a user is created."""
    if kwargs['created']:
        face_verification_object = FaceVerificationManager(user=kwargs['instance'])
        face_verification_object.save()

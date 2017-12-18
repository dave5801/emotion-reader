"""Models for user profile."""
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django import forms
from django.forms import ModelForm


class EmotionProfile(models.Model):
    """The imager profile model."""

    objects = models.Manager
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='profile')
    cover = models.ImageField(upload_to='documents/%Y/%m/%d',
                              blank=True,
                              null=True)

    def __str__(self):
        """Print function returns this."""
        return self.user.username


@receiver(models.signals.post_save, sender=User)
def create_profile(sender, **kwargs):
    """Create the profile when a user is created."""
    if kwargs['created']:
        profile = EmotionProfile(user=kwargs['instance'])
        profile.save()


class EmotionProfileForm(ModelForm):
    """Form for an EmotionProfile."""

    email = forms.CharField(max_length=User._meta.get_field('email').max_length,
                            widget=forms.widgets.EmailInput())

    first_name = forms.CharField(max_length=User._meta.get_field('first_name').max_length,
                                 required=False)

    last_name = forms.CharField(max_length=User._meta.get_field('last_name').max_length,
                                required=False)

    # cover = forms.ImageField(upload_to='documents/%Y/%m/%d',
    #                          blank=True,
    #                          null=True)

    class Meta:
        """Meta."""

        model = EmotionProfile
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        """Limit photos to only those by the user."""
        username = kwargs.pop('username')
        super(EmotionProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].initial = User.objects.get(username=username).email
        self.fields['first_name'].initial = User.objects.get(username=username).first_name
        self.fields['last_name'].initial = User.objects.get(username=username).last_name
        # self.fields['cover'].initial = EmotionProfile.cover

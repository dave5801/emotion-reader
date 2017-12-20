"""Emotion model."""
from django.db import models
from django.contrib.auth.models import User


class Emotion(models.Model):
    """The emotion model."""

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='emotions')

    date_recorded = models.DateTimeField(auto_now=True)

    anger = models.FloatField()
    contempt = models.FloatField()
    disgust = models.FloatField()
    fear = models.FloatField()
    happiness = models.FloatField()
    neutral = models.FloatField()
    sadness = models.FloatField()
    surprise = models.FloatField()

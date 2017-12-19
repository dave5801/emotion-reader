"""Models for journal."""
from django.db import models
from django.contrib.auth.models import User


class Journal(models.Model):
    """The journal model."""

    objects = models.Manager
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='journal')
    title = models.CharField(max_length=50)
    body = models.TextField(max_length=500)
    date = models.DateField(auto_now_add=True)

"""Config for admin."""
from django.contrib import admin
from emotion_emotions.models import Emotion

admin.site.register(Emotion)

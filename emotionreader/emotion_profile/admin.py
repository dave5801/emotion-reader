"""Config for admin."""
from django.contrib import admin
from emotion_profile.models import EmotionProfile

admin.site.register(EmotionProfile)

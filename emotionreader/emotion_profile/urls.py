"""URLS for profile."""
from django.conf.urls import url, include
from django.contrib import admin
from emotion_profile.views import ProfileView

urlpatterns = [
    url(r'^$',
        ProfileView.as_view(template_name='emotion_profile/profile.html'),
        name='profile'),
]

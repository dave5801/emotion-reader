"""URLS for profile."""
from django.conf.urls import url, include
from django.contrib import admin
from emotion_profile.views import ProfileView, UpdateProfile

urlpatterns = [
    url(r'^$',
        ProfileView.as_view(template_name='emotion_profile/profile.html'),
        name='profile'),
    url(r'^edit/(?P<pk>\d+)$',
        UpdateProfile.as_view(),
        name='update_profile')
]

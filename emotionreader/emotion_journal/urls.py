"""URLS for profile."""
from django.conf.urls import url, include
from django.contrib import admin
from emotion_journal.views import JournalView, CreateJournal

urlpatterns = [
    url(r'^$',
        JournalView.as_view(),
        name='journal'),
    url(r'^create/$',
        CreateJournal.as_view(),
        name='create_journal')
]

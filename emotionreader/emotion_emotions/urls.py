"""URLs for emotion app."""
from django.conf.urls import url
from emotion_emotions.views import EmotionAnalysis, RecordEmotions

urlpatterns = [
    url(r'^analysis$', EmotionAnalysis.as_view(), name='emotion_analusis'),
    url(r'^record$', RecordEmotions.as_view(), name='record_emotions')
]

"""URLs for emotion app."""
from django.conf.urls import url
from emotion_emotions.views import EmotionAnalysis, RecordEmotions, EmotionDateHistory

urlpatterns = [
    url(r'^analysis$', EmotionAnalysis.as_view(), name='emotion_analysis'),
    url(r'^record$', RecordEmotions.as_view(), name='record_emotions'),
    url(r'^history/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})$',
        EmotionDateHistory.as_view(), name='emotion_history')
]

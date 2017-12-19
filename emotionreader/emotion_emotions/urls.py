from django.conf.urls import url
from emotion_emotions.views import RecordEmotions

urlpatterns = [
    url(r'^record$', RecordEmotions.as_view(), name='record_emotions')
]

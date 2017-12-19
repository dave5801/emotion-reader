from django.conf.urls import url
from emotion_emotions.views import ImageCapView

urlpatterns = [
    url(r'^imagecap$', ImageCapView.as_view(), name='imagecap')
]

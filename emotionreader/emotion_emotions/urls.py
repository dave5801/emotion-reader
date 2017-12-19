"""URLs for emotion app."""
from django.conf.urls import url
from emotion_emotions.views import ImageCapView, save_image, EmotionAnalysis

urlpatterns = [
    url(r'^imagecap$', ImageCapView.as_view(), name='imagecap'),
    url(r'^savecap$', save_image, name='savecap'),
    url(r'^analysis$', EmotionAnalysis.as_view(), name='emotion_analusis'),
]

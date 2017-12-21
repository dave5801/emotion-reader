"""Views."""
from django.views.generic import ListView, TemplateView
from emotion_profile.models import EmotionProfile
# from django.conf import settings


class HomeView(ListView):
    """Home page view."""

    model = EmotionProfile
    template_name = 'emotionreader/home.html'


class AboutView(TemplateView):
    """The about view."""

    template_name = 'emotionreader/about.html'

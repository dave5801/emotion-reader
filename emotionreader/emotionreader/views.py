"""Views."""
from django.views.generic import TemplateView


class HomeView(TemplateView):
    """Home page view."""

    template_name = 'emotionreader/home.html'


class AboutView(TemplateView):
    """The about view."""

    template_name = 'emotionreader/about.html'

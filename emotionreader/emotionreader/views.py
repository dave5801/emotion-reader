"""Views."""

from django.views.generic import TemplateView
# from django.conf import settings


class HomeView(TemplateView):
    """Home page view."""

    template_name = 'emotionreader/home.html'

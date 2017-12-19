"""Process for submitting image for evaluation."""
from django.shortcuts import render
from django.views.generic import TemplateView


class ImageCapView(TemplateView):
    """Capture the image for evaulation."""

    template_name = 'emotion_emotions/imageCap.html'

    # def get_context_data(self):
    #     """."""
    #     # context = super(HomeView, self).get_context_data()  # get_context_data is built in method of Template View.
    #     # photos = Photo.objects.all()
    #     # context['photos'] = photos
    #     # return context

"""Process for submitting image for evaluation."""
from django.conf import settings
from django.views.generic import TemplateView
from django.http import HttpResponse

from base64 import b64decode
import os


class ImageCapView(TemplateView):
    """Capture the image for evaulation."""

    template_name = 'emotion_emotions/imageCap.html'

    # def get_context_data(self):
    #     """."""
    #     # context = super(HomeView, self).get_context_data()  # get_context_data is built in method of Template View.
    #     # photos = Photo.objects.all()
    #     # context['photos'] = photos
    #     # return context


def save_image(request):
    """Save the image to the media directory."""
    image = request.POST['image'].split(',', maxsplit=1)[1]
    image = b64decode(image)
    with open(os.path.join(settings.MEDIA_ROOT, 'testfile.jpg'), 'wb') as f:
        f.write(image)
    return HttpResponse('Complete')

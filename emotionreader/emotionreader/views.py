from django.contrib.auth.models import User
from django.views import View
from django.views.generic import TemplateView
"""Views."""
from django.views.generic import ListView
from emotion_profile.models import EmotionProfile
from base64 import b64decode
from django.http import HttpResponse, HttpResponseBadRequest
# from django.conf import settings


class HomeView(ListView):
    """Home page view."""

    model = EmotionProfile
    template_name = 'emotionreader/home.html'
    # context_object_name = 'data'

    # def get_context_data(self, **kwargs):
    #     """."""
    #     context = super(HomeView, self).get_context_data(**kwargs)
    #     return context

class FaceVerificationView(TemplateView):

    model = User
    template_name = 'registration/face_verification.html'

    def post(self, request, *args, **kwargs):
        """Extract emotions from posted image."""
        try:
            image = request.POST['image'].split(',', maxsplit=1)[1]
            image = b64decode(image)
        except (KeyError, IndexError):
            return HttpResponseBadRequest('Invalid data.')

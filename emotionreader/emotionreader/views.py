"""Views."""
from django.views.generic import ListView
from emotion_profile.models import EmotionProfile
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

class FaceVerificationView():

    model = User
    template_name = 'registration/face_verification.html'
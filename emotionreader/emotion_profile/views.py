"""Views for profile."""
from django.views.generic import TemplateView, UpdateView
from django.core.urlresolvers import reverse_lazy
from emotion_profile.models import EmotionProfile


class ProfileView(TemplateView):
    """Profile view."""

    def get_context_data(self, pk=None):
        """Get context data for view."""
        # photo = Photo.objects.get(id=pk)
        # return {'photo': photo}


class UpdateProfile(UpdateView):
    """Update profile view."""

    model = EmotionProfile
    template_name = 'emotion_profile/update_profile.html'
    fields = []
    success_url = reverse_lazy('profile')

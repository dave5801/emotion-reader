"""Views for profile."""
from django.views.generic import TemplateView


class ProfileView(TemplateView):
    """Profile view."""

    def get_context_data(self, pk=None):
        """Get context data for view."""
        # photo = Photo.objects.get(id=pk)
        # return {'photo': photo}

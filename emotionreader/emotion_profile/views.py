"""Views for profile."""
from django.views.generic import DetailView, UpdateView
from django.core.urlresolvers import reverse_lazy
from emotion_profile.models import EmotionProfile, EmotionProfileForm
from django.shortcuts import redirect


class ProfileView(DetailView):
    """Profile view."""

    template_name = 'emotion_profile/profile.html'
    model = EmotionProfile
    slug_field = 'user__username'
    slug_url_kwarg = 'username'

    def get(self, *args, **kwargs):
        """Redirect home if not logged in."""
        self.kwargs['username'] = self.request.user.get_username()
        if self.kwargs['username'] == '':
            return redirect('home')

        return super(ProfileView, self).get(*args, **kwargs)


class UpdateProfile(UpdateView):
    """Update profile view."""

    model = EmotionProfile
    template_name = 'emotion_profile/update_profile.html'
    success_url = reverse_lazy('profile')
    login_url = reverse_lazy('login')

    slug_field = 'user__username'
    slug_url_kwarg = 'username'
    form_class = EmotionProfileForm

    def get_form_kwargs(self):
        """Update the kwargs to include the current user's username."""
        kwargs = super(UpdateProfile, self).get_form_kwargs()
        kwargs.update({'username': self.request.user.username})
        return kwargs

    def get(self, *args, **kwargs):
        """Redirect home if not logged in."""
        self.kwargs['username'] = self.request.user.get_username()
        if self.kwargs['username'] == '':
            return redirect('home')

        return super(UpdateProfile, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        """Redirect home if not logged in."""
        self.kwargs['username'] = self.request.user.get_username()
        if self.kwargs['username'] == '':
            return redirect('home')

        return super(UpdateProfile, self).post(*args, **kwargs)

    def form_valid(self, form):
        """Assign user as Edit of profile."""
        form.instance.user.email = form.data['email']
        form.instance.user.first_name = form.data['first_name']
        form.instance.user.last_name = form.data['last_name']
        form.instance.user.save()
        return super(UpdateProfile, self).form_valid(form)

"""Views for profile."""
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from emotion_profile.models import EmotionProfile, EmotionProfileForm
from django.shortcuts import redirect
import time
import operator


class ProfileView(LoginRequiredMixin, DetailView):
    """Profile view."""

    template_name = 'emotion_profile/profile.html'
    model = EmotionProfile
    slug_field = 'user__username'
    slug_url_kwarg = 'username'
    login_url = reverse_lazy('login')

    def get_context_data(self, *args, **kwargs):
        """Send data to profile."""
        user = self.request.user
        context = super(ProfileView, self).get_context_data()

        emotions = user.emotions.all()

        dates = []
        anger = []
        contempt = []
        disgust = []
        fear = []
        happiness = []
        neutral = []
        sadness = []
        surprise = []

        for emotion in emotions:
            dates.append(int(time.mktime(emotion.date_recorded.timetuple())) * 1000)
            anger.append(emotion.anger * 100)
            contempt.append(emotion.contempt * 100)
            disgust.append(emotion.disgust * 100)
            fear.append(emotion.fear * 100)
            happiness.append(emotion.happiness * 100)
            neutral.append(emotion.neutral * 100)
            sadness.append(emotion.sadness * 100)
            surprise.append(emotion.surprise * 100)

        context['avg_anger'] = float("{0:.2f}".format(sum(anger) / float(len(anger) or 1)))
        context['avg_contempt'] = float("{0:.2f}".format(sum(contempt) / float(len(contempt) or 1)))
        context['avg_disgust'] = float("{0:.2f}".format(sum(disgust) / float(len(disgust) or 1)))
        context['avg_fear'] = float("{0:.2f}".format(sum(fear) / float(len(fear) or 1)))
        context['avg_happiness'] = float("{0:.2f}".format(sum(happiness) / float(len(happiness) or 1)))
        context['avg_neutral'] = float("{0:.2f}".format(sum(neutral) / float(len(neutral) or 1)))
        context['avg_sadness'] = float("{0:.2f}".format(sum(sadness) / float(len(sadness) or 1)))
        context['avg_surprise'] = float("{0:.2f}".format(sum(surprise) / float(len(surprise) or 1)))

        last_moods = {'anger': anger[-1],
                      'contempt': contempt[-1],
                      'disgust': disgust[-1],
                      'fear': fear[-1],
                      'happiness': happiness[-1],
                      'neutral': neutral[-1],
                      'sadness': sadness[-1],
                      'surprise': surprise[-1]
                      }

        context['mood'] = max(last_moods, key=last_moods.get)

        return context

    def get(self, *args, **kwargs):
        """Redirect home if not logged in."""
        self.kwargs['username'] = self.request.user.get_username()

        return super(ProfileView, self).get(*args, **kwargs)


class UpdateProfile(LoginRequiredMixin, UpdateView):
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

        return super(UpdateProfile, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        """Redirect home if not logged in."""
        self.kwargs['username'] = self.request.user.get_username()

        return super(UpdateProfile, self).post(*args, **kwargs)

    def form_valid(self, form):
        """Assign user as Edit of profile."""
        form.instance.user.email = form.data['email']
        form.instance.user.first_name = form.data['first_name']
        form.instance.user.last_name = form.data['last_name']
        form.instance.user.save()
        return super(UpdateProfile, self).form_valid(form)

"""Process for submitting image for evaluation."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import TemplateView, ListView
from django.utils import timezone
from emotion_emotions.models import Emotion
from emotion_journal.models import Journal
import numpy as np
from datetime import datetime

from base64 import b64decode
import math
import os
import requests
import time


class EmotionDateHistory(LoginRequiredMixin, ListView):
    """View for a single day."""

    model = Emotion
    template_name = 'emotion_emotions/history.html'

    def get_queryset(self):
        """Limit to logged in user's records."""
        all_emotions = Emotion.objects.filter(user=self.request.user)
        return all_emotions.filter(date_recorded__year=self.kwargs['year'],
                                   date_recorded__month=self.kwargs['month'],
                                   date_recorded__day=self.kwargs['day'],)

    def get_context_data(self, **kwargs):
        """Get context data and add default cover."""
        context = super(EmotionDateHistory, self).get_context_data(**kwargs)

        dates = []
        anger = []
        contempt = []
        disgust = []
        fear = []
        happiness = []
        neutral = []
        sadness = []
        surprise = []

        for emotion in context['object_list']:
            dates.append(int(time.mktime(emotion.date_recorded.timetuple())) * 1000)
            anger.append(emotion.anger * 100)
            contempt.append(emotion.contempt * 100)
            disgust.append(emotion.disgust * 100)
            fear.append(emotion.fear * 100)
            happiness.append(emotion.happiness * 100)
            neutral.append(emotion.neutral * 100)
            sadness.append(emotion.sadness * 100)
            surprise.append(emotion.surprise * 100)

        context['dates'] = dates
        date = datetime.strptime('{}{}{}'.format(self.kwargs['day'], self.kwargs['month'], self.kwargs['year']), '%d%m%Y')
        context['date'] = date.strftime('%A, %B %d, %Y')

        context['anger'] = anger
        context['contempt'] = contempt
        context['disgust'] = disgust
        context['fear'] = fear
        context['happiness'] = happiness
        context['neutral'] = neutral
        context['sadness'] = sadness
        context['surprise'] = surprise
        context['avg_anger'] = sum(anger) / float(len(anger) or 1)
        context['avg_contempt'] = sum(contempt) / float(len(contempt) or 1)
        context['avg_disgust'] = sum(disgust) / float(len(disgust) or 1)
        context['avg_fear'] = sum(fear) / float(len(fear) or 1)
        context['avg_happiness'] = sum(happiness) / float(len(happiness) or 1)
        context['avg_neutral'] = sum(neutral) / float(len(neutral) or 1)
        context['avg_sadness'] = sum(sadness) / float(len(sadness) or 1)
        context['avg_surprise'] = sum(surprise) / float(len(surprise) or 1)

        full_journal = Journal.objects.filter(user=self.request.user)
        entries = full_journal.filter(date__year=self.kwargs['year'],
                                      date__month=self.kwargs['month'],
                                      date__day=self.kwargs['day'],)

        context['entries'] = entries

        return context


class EmotionAnalysis(LoginRequiredMixin, TemplateView):
    """View for emotion analysis."""

    template_name = 'emotion_emotions/emotion_analysis.html'

    def get_context_data(self):
        """Load a plot to the view."""
        user = self.request.user
        context = super(EmotionAnalysis, self).get_context_data()

        emotions = user.emotions.all().order_by('date_recorded')

        dates = []
        anger = []
        contempt = []
        disgust = []
        fear = []
        happiness = []
        neutral = []
        sadness = []
        surprise = []

        for emotion in emotions:  #pragma: nocover
            dates.append(int(time.mktime(emotion.date_recorded.timetuple())) * 1000)
            anger.append(emotion.anger * 100)
            contempt.append(emotion.contempt * 100)
            disgust.append(emotion.disgust * 100)
            fear.append(emotion.fear * 100)
            happiness.append(emotion.happiness * 100)
            neutral.append(emotion.neutral * 100)
            sadness.append(emotion.sadness * 100)
            surprise.append(emotion.surprise * 100)

        log_anger = [math.log(x, 100) * 100 for x in anger]
        log_contempt = [math.log(x, 100) * 100 for x in contempt]
        log_disgust = [math.log(x, 100) * 100 for x in disgust]
        log_fear = [math.log(x, 100) * 100 for x in fear]
        log_happiness = [math.log(x, 100) * 100 for x in happiness]
        log_neutral = [math.log(x, 100) * 100 for x in neutral]
        log_sadness = [math.log(x, 100) * 100 for x in sadness]
        log_surprise = [math.log(x, 100) * 100 for x in surprise]

        if dates:
            date = emotions.first().date_recorded
            delta = timezone.now() - date
            days_ago = delta.days + (delta.seconds / 86400)
        else:
            days_ago = 0.0

        context['days_ago'] = "%.1f" % days_ago
        context['dates'] = dates

        context['log_anger'] = log_anger
        context['log_contempt'] = log_contempt
        context['log_disgust'] = log_disgust
        context['log_fear'] = log_fear
        context['log_happiness'] = log_happiness
        context['log_neutral'] = log_neutral
        context['log_sadness'] = log_sadness
        context['log_surprise'] = log_surprise

        context['anger'] = anger
        context['contempt'] = contempt
        context['disgust'] = disgust
        context['fear'] = fear
        context['happiness'] = happiness
        context['neutral'] = neutral
        context['sadness'] = sadness
        context['surprise'] = surprise
        context['avg_anger'] = sum(anger) / float(len(anger) or 1)
        context['avg_contempt'] = sum(contempt) / float(len(contempt) or 1)
        context['avg_disgust'] = sum(disgust) / float(len(disgust) or 1)
        context['avg_fear'] = sum(fear) / float(len(fear) or 1)
        context['avg_happiness'] = sum(happiness) / float(len(happiness) or 1)
        context['avg_neutral'] = sum(neutral) / float(len(neutral) or 1)
        context['avg_sadness'] = sum(sadness) / float(len(sadness) or 1)
        context['avg_surprise'] = sum(surprise) / float(len(surprise) or 1)

        return context


class RecordEmotions(LoginRequiredMixin, TemplateView):
    """Capture the current emotions and record to database."""

    template_name = 'emotion_emotions/imageCap.html'
    login_url = reverse_lazy('login')

    def get_emotion_data(self, image):
        """Get the emotion data from the API for the image."""
        headers = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': os.environ.get('EMOTION_API_KEY', '')
        }

        url = 'https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize'

        response = requests.post(url, headers=headers, data=image)

        return response.json()

    def post(self, request, *args, **kwargs):
        """Extract emotions from posted image."""
        try:
            image = request.POST['image'].split(',', maxsplit=1)[1]
            image = b64decode(image)
        except (KeyError, IndexError):
            return HttpResponseBadRequest('Invalid data.')

        if request.user.faces.auth_face:
            verifier = request.user.faces
            new_face = verifier.detected(image, img_stream=True)[0]['faceId']
            correct_face = verifier.verify_against_registration(new_face)

            if not correct_face:
                return HttpResponseBadRequest('Face does not belong to user.')

        data = self.get_emotion_data(image)

        if 'error' in data:
            return HttpResponseBadRequest(data['error']['message'])

        if len(data) == 0:
            return HttpResponseBadRequest('No face detected.')

        data = data[0]['scores']

        emotion = Emotion(user=self.request.user)
        emotion.anger = data['anger']
        emotion.contempt = data['contempt']
        emotion.disgust = data['disgust']
        emotion.fear = data['fear']
        emotion.happiness = data['happiness']
        emotion.neutral = data['neutral']
        emotion.sadness = data['sadness']
        emotion.surprise = data['surprise']
        emotion.save()

        return HttpResponse('Emotions Recorded')


76-85
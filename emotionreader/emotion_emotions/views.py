"""Process for submitting image for evaluation."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import TemplateView
from emotion_emotions.models import Emotion

from bokeh.plotting import figure
from bokeh.embed import components

from base64 import b64decode
import os
import requests
import time


class EmotionAnalysis(TemplateView):
    """View for emotion analysis."""

    template_name = 'emotion_emotions/emotion_analysis.html'

    def get_context_data(self):
        """Load a plot to the view."""
        user = self.request.user
        context = super(EmotionAnalysis, self).get_context_data()

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

        context['dates'] = dates
        context['anger'] = anger
        context['contempt'] = contempt
        context['disgust'] = disgust
        context['fear'] = fear
        context['happiness'] = happiness
        context['neutral'] = neutral
        context['sadness'] = sadness
        context['surprise'] = surprise
        context['avg_anger'] = sum(anger) / float(len(anger))
        context['avg_contempt'] = sum(contempt) / float(len(contempt))
        context['avg_disgust'] = sum(disgust) / float(len(disgust))
        context['avg_fear'] = sum(fear) / float(len(fear))
        context['avg_happiness'] = sum(happiness) / float(len(happiness))
        context['avg_neutral'] = sum(neutral) / float(len(neutral))
        context['avg_sadness'] = sum(sadness) / float(len(sadness))
        context['avg_surprise'] = sum(surprise) / float(len(surprise))

        return context


class RecordEmotions(TemplateView, LoginRequiredMixin):
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

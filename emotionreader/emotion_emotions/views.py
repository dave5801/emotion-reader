"""Process for submitting image for evaluation."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import TemplateView
from emotion_emotions.models import Emotion

from base64 import b64decode
import os
import requests


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

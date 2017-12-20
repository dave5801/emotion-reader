"""Process for submitting image for evaluation."""
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseBadRequest
from emotion_emotions.models import Emotion

from bokeh.plotting import figure
from bokeh.embed import components

from base64 import b64decode
import os
import requests


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
            dates.append(emotion.date_recorded)
            anger.append(emotion.anger)
            contempt.append(emotion.contempt)
            disgust.append(emotion.disgust)
            fear.append(emotion.fear)
            happiness.append(emotion.happiness)
            neutral.append(emotion.neutral)
            sadness.append(emotion.sadness)
            surprise.append(emotion.surprise)

        p = figure(title="Emotions vs. Time",
                   x_axis_label='Time',
                   y_axis_label='Emotions',
                   x_axis_type='datetime')
        p.line(dates,
               anger,
               legend="Anger",
               line_width=2,
               line_color='red')
        p.line(dates,
               contempt,
               legend="Contempt",
               line_width=2,
               line_color='green')
        p.line(dates,
               disgust,
               legend="Disgust",
               line_width=2,
               line_color='brown')
        p.line(dates,
               fear,
               legend="Fear",
               line_width=2,
               line_color='purple')
        p.line(dates,
               happiness,
               legend="Happiness",
               line_width=2,
               line_color='yellow')
        p.line(dates,
               neutral,
               legend="Neutral",
               line_width=2,
               line_color='gray')
        p.line(dates,
               sadness,
               legend="Sadness",
               line_width=2,
               line_color='blue')
        p.line(dates,
               surprise,
               legend="Surprise",
               line_width=2,
               line_color='orange')

        script, div = components(p)

        context['plot_html'] = div
        context['plot_script'] = script
        # context['dates'] = dates
        context['anger'] = anger
        context['contempt'] = contempt
        return context


class RecordEmotions(TemplateView):
    """Capture the current emotions and record to database."""

    template_name = 'emotion_emotions/imageCap.html'

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
        except KeyError:
            return HttpResponseBadRequest('Invalid image.')

        data = self.get_emotion_data(image)

        if 'error' in data:
            return HttpResponseBadRequest(data['error']['message'])

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

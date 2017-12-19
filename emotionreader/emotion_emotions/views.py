"""Process for submitting image for evaluation."""
from django.conf import settings
from django.views.generic import TemplateView
from django.http import HttpResponse

from bokeh.plotting import figure
from bokeh.embed import components

from base64 import b64decode
import os


class ImageCapView(TemplateView):
    """Capture the image for evaulation."""

    template_name = 'emotion_emotions/imageCap.html'

    # def get_context_data(self):
    #     """."""
    #     # context = super(HomeView, self).get_context_data()  # get_context_data is built in method of Template View.
    #     # photos = Photo.objects.all()
    #     # context['photos'] = photos
    #     # return context


def save_image(request):
    """Save the image to the media directory."""
    image = request.POST['image'].split(',', maxsplit=1)[1]
    image = b64decode(image)
    with open(os.path.join(settings.MEDIA_ROOT, 'testfile.jpg'), 'wb') as f:
        f.write(image)
    return HttpResponse('Complete')


class EmotionAnalysis(TemplateView):
    """View for emotion analysis."""

    template_name = 'emotion_emotions/emotion_analysis.html'

    def get_context_data(self):
        """Load a plot to the view."""
        context = super(EmotionAnalysis, self).get_context_data()

        x = [1, 2, 3, 4, 5]
        y = [6, 7, 2, 4, 5]

        p = figure(title="Emotions vs. Time", x_axis_label='Time', y_axis_label='Emotions')

        p.line(x, y, legend="Anger", line_width=2, line_color='red')
        p.line(x, y, legend="Contempt", line_width=2, line_color='blue')
        p.line(x, y, legend="Disgust", line_width=2, line_color='blue')
        p.line(x, y, legend="Fear", line_width=2, line_color='blue')
        p.line(x, y, legend="Happiness", line_width=2, line_color='blue')
        p.line(x, y, legend="Neutral", line_width=2, line_color='blue')
        p.line(x, y, legend="Sadness", line_width=2, line_color='blue')
        p.line(x, y, legend="Surprise", line_width=2, line_color='blue')

        script, div = components(p)

        context['plot_html'] = div
        context['plot_script'] = script

        return context

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

        p = figure(title="simple line example", x_axis_label='x', y_axis_label='y')

        p.line(x, y, legend="Temp.", line_width=2)

        script, div = components(p)

        context['plot_html'] = div
        context['plot_script'] = script

        return context

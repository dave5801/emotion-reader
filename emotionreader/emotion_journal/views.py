"""Views for journal."""
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView
from emotion_journal.models import Journal
from django.core.urlresolvers import reverse_lazy


class JournalView(ListView):
    """Journal view."""

    context_object_name = 'entries'
    template_name = 'emotion_journal/journal.html'
    queryset = Journal.objects.all()

    # def get(self, *args, **kwargs):
    #     """Redirect home if not logged in."""
    #     self.kwargs['username'] = self.request.user.get_username()
    #     if self.kwargs['username'] == '':
    #         return redirect('home')

    #     return super(EmotionJournal, self).get(*args, **kwargs)


class CreateJournal(CreateView):
    """View to create new journal entry."""

    model = Journal
    template_name = 'emotion_journal/create_journal.html'
    fields = ['title', 'body']
    success_url = reverse_lazy('journal')

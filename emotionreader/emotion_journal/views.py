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

    def get_queryset(self, user=None):
        """Get queryset for photos."""
        return Journal.objects.filter(user__username=user)

    def get_context_data(self):
        """Get the user's photos and albums."""
        context = super(JournalView, self).get_context_data()
        user = self.request.user.get_username()
        entries = Journal.objects.filter(user__username=user).order_by('date')
        context['entries'] = entries

        return context


class CreateJournal(CreateView):
    """View to create new journal entry."""

    model = Journal
    login_url = reverse_lazy('login')
    template_name = 'emotion_journal/create_journal.html'
    fields = ['title', 'body']
    success_url = reverse_lazy('journal')

    def form_valid(self, form):
        """Assign user as creater of journal."""
        form.instance.user = self.request.user
        return super(CreateJournal, self).form_valid(form)

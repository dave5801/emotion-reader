"""Views for journal."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from emotion_journal.models import Journal
from django.core.urlresolvers import reverse_lazy


class JournalView(LoginRequiredMixin, ListView):
    """Journal view."""

    template_name = 'emotion_journal/journal.html'
    context_object_name = 'entries'
    model = Journal

    def get_queryset(self, user=None):
        """Get queryset for photos."""
        return Journal.objects.filter(user__username=user)

    def get_context_data(self):
        """Get the user's photos and albums."""
        context = super(JournalView, self).get_context_data()
        user = self.request.user.get_username()
        entries = self.get_queryset(user).order_by('date')
        context['entries'] = entries[::-1]
        return context


class CreateJournal(LoginRequiredMixin, CreateView):
    """View to create new journal entry."""

    model = Journal
    login_url = reverse_lazy('login')
    template_name = 'emotion_journal/create_journal.html'
    fields = ['title', 'body']
    success_url = reverse_lazy('journal')

    def form_valid(self, form):
        """Assign user as creator of journal."""
        form.instance.user = self.request.user
        return super(CreateJournal, self).form_valid(form)

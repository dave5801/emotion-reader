"""Tests for the imagersite routes."""
from django.conf import settings
from django.test import TestCase, RequestFactory, override_settings
from django.urls import reverse_lazy
from emotion_journal.models import Journal
from emotion_profile.tests import UserFactory


class JournalViewUnitTests(TestCase):
    """Tests for the functions of the Journal section of the Emotion app."""


class MainRoutingTests(TestCase):
    """Tests for the Journal route in the Emotion App."""

    def setUp(self):
        """Set up a user for testing login.."""
        user = UserFactory(username='mike', email='mike@ike.net')
        user.set_password('password')
        user.save()

    def test_journal_route_has_200_response(self):
        """Test that home route has a 200 response code."""
        self.client.login(username='mike', password='password')
        response = self.client.get(reverse_lazy('journal'))
        self.assertEqual(response.status_code, 200)

    def test_create_journal_route_has_200_response(self):
        """Test that home route has a 200 response code."""
        self.client.login(username='mike', password='password')
        response = self.client.get(reverse_lazy('create_journal'))
        self.assertEqual(response.status_code, 200)

    def test_journal_route_has_heading(self):
        """Test that journal route has a heading on the page."""
        self.client.login(username='mike', password='password')
        response = self.client.get(reverse_lazy('journal'))
        self.assertIn(b'Emotion Journal', response.content)

    def test_create_journal_route_has_heading(self):
        """Test that create journal route has a heading on the page."""
        self.client.login(username='mike', password='password')
        response = self.client.get(reverse_lazy('create_journal'))
        self.assertIn(b'Create Journal', response.content)

    def test_journal_route_accessible_only_if_logged_in(self):
        """Test that a user can only see their journal page if logged in here."""
        response = self.client.get(reverse_lazy('journal'))
        self.assertEqual(response.status_code, 302)

    def test_journal_route_accessible_when_logged_in(self):
        """Test that a user can only see their journal page if logged in here."""
        self.client.login(username='mike', password='password')
        response = self.client.get(reverse_lazy('journal'))
        self.assertEqual(response.status_code, 200)

    def test_create_journal_route_accessible_only_if_logged_in(self):
        """Test that a user can only see their  create journal page if logged in here."""
        response = self.client.get(reverse_lazy('create_journal'))
        self.assertEqual(response.status_code, 302)

    def test_create_journal_route_accessible_when_logged_in(self):
        """Test that a user can only create a journal entry if logged."""
        self.client.login(username='mike', password='password')
        response = self.client.get(reverse_lazy('create_journal'))
        self.assertEqual(response.status_code, 200)

    def test_form_valid(self):
        """Test if form is correctly assigned to user."""
        self.client.login(username='mike', password='password')
        form = {'title': 'Merry Christmas!',
                'body': 'Happy New Year!'}
        response = self.client.post(reverse_lazy('create_journal'),
                                    form)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse_lazy('journal'))

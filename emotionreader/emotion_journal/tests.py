"""Tests for the imagersite routes."""
from django.conf import settings
from django.test import TestCase, RequestFactory, override_settings
from django.urls import reverse_lazy
from emotion_journal.models import Journal
from emotion_profile.tests import UserFactory

import os


class JournalViewUnitTests(TestCase):
    """Tests for the functions of the Journal section of the Emotion app."""

    @classmethod
    def setUpClass(cls):
        """Set up a dummy request."""
        super(JournalViewUnitTests, cls).setUpClass()
        os.system('mkdir {}'.format(
            os.path.join(settings.BASE_DIR, 'test_media_for_home')
        ))

    @classmethod
    def tearDownClass(cls):
        """Remove the test directory."""
        super(JournalViewUnitTests, cls).tearDownClass()
        os.system('rm -rf {}'.format(
            os.path.join(settings.BASE_DIR, 'test_media_for_home')
        ))


# @override_settings(MEDIA_ROOT=os.path.join(settings.BASE_DIR,
#                        'test_media_for_home'))
#     def test_home_view_returns_context_with_photo_from_db(self):
#         """Test that the homeview  returns photo from db."""
#         from emotion_journal.views import JournalView
#         user = UserFactory()
#         user.set_password('password')
#         user.save()
#         photo = PhotoFactory(user=user, title='test', published='PUBLIC')
#         photo.save()
#         view = HomeView()
#         data = view.get_context_data()
#         self.assertIn('hero_img_url', data)
#         self.assertEqual('test', data['hero_img_title'])


class MainRoutingTests(TestCase):
    """Tests for the Journal route in the Emotion App."""

    def setUp(self):
        """Set up a user for testing login.."""
        user = UserFactory(username='mike', email='mike@ike.net')
        user.set_password('password')
        user.save()

    def test_journal_route_has_200_response(self):
        """Test that home route has a 200 response code."""
        response = self.client.get(reverse_lazy('journal'))
        self.assertEqual(response.status_code, 200)

    def test_create_journal_route_has_200_response(self):
        """Test that home route has a 200 response code."""
        response = self.client.get(reverse_lazy('create_journal'))
        self.assertEqual(response.status_code, 200)

    def test_journal_route_has_heading(self):
        """Test that journal route has a heading on the page."""
        response = self.client.get(reverse_lazy('journal'))
        self.assertIn(b'Emotion Journal', response.content)

    def test_create_journal_route_has_heading(self):
        """Test that create journal route has a heading on the page."""
        response = self.client.get(reverse_lazy('create_journal'))
        self.assertIn(b'Create Journal', response.content)

    def test_journal_route_accessible_only_if_logged_in(self):
        """Test that a user can only see their journal page if logged in here."""
        response = self.client.get(reverse_lazy('journal'))
        self.assertEqual(response.status_code, 302)

    def test_create_journal_route_accessible_only_if_logged_in(self):
        """Test that a user can only see their  create journal page if logged in here."""
        response = self.client.get(reverse_lazy('create_journal'))
        self.assertEqual(response.status_code, 302)

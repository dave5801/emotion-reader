"""Test emotion app."""
from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from emotion_emotions.models import Emotion
from emotion_profile.tests import UserFactory
from base64 import b64decode
from datetime import datetime
from unittest.mock import patch
import factory
import random


class EmotionFactory(factory.django.DjangoModelFactory):
    """Factory for fake User."""

    class Meta:
        """Meta."""

        model = Emotion

    anger = random.random()
    contempt = random.random()
    disgust = random.random()
    fear = random.random()
    happiness = random.random()
    neutral = random.random()
    sadness = random.random()
    surprise = random.random()


class EmotionTest(TestCase):
    """Test the emotion app."""

    @classmethod
    def setUpClass(cls):
        """Add one minimal user to the database."""
        super(EmotionTest, cls).setUpClass()
        user = UserFactory(username='dan', email='dan@dan.net')
        user.set_password('password')
        user.first_name = 'Dan'
        user.last_name = 'Theman'
        user.save()
        cls.dan = user

        for _ in range(10):
            user = UserFactory.create()
            user.set_password(factory.Faker('password'))
            user.save()

    def test_emotion_is_created_and_attached_to_user(self):
        """Test that an emotion is created and attached to a user."""
        one_user = User.objects.last()

        emotion = EmotionFactory(user=one_user, anger=.1)
        emotion.save()

        self.assertEqual(one_user.emotions.first().anger, .1)

    def test_emotion_has_date_recorded(self):
        """Test that the emotion has a date-recorded that is now by default."""
        emotion = EmotionFactory(user=self.dan)
        emotion.save()

        one_emotion = Emotion.objects.first()
        now = datetime.now().strftime('%x %X')[:2]
        self.assertEqual(one_emotion.date_recorded.strftime('%x %X')[:2], now)


class EmotionViewTests(TestCase):
    """Test the Emotion View class methods."""

    def setUp(self):
        """Create a dummy user."""
        from emotion_emotions.views import RecordEmotions

        user = UserFactory(username='dan', email='dan@dan.net')
        user.set_password('password')
        user.first_name = 'Dan'
        user.last_name = 'Theman'
        user.save()
        self.dan = user

        self.request = RequestFactory()

        mock_emotions = [
            {'scores': {
                'anger': 1.00,
                'contempt': 1.00,
                'disgust': 1.00,
                'fear': 1.00,
                'happiness': 1.00,
                'neutral': 1.00,
                'sadness': 1.00,
                'surprise': 1.00,
            }}
        ]

        emotion_patcher = patch.object(RecordEmotions, 'get_emotion_data',
                                       return_value=mock_emotions)
        self.mock_emotion_api_call = emotion_patcher.start()
        self.addCleanup(emotion_patcher.stop)
        self.emotion_patcher = emotion_patcher

    #     self.assertEqual(one_user.emotion.last().anger, 1.73134707e-09)

    # Do not want to ping API every test
    # def test_get_emotion_data_extracts_emotion_data(self):
    #     """Test that get_emotion_data extracts the data from an image."""
    #     from emotion_emotions.views import RecordEmotions
    #     self.emotion_patcher.stop()
    #     request = self.request.get('')
    #     request.user = self.dan
    #     image = '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'
    #     view = RecordEmotions(request=request)
    #     data = view.get_emotion_data(b64decode(image))
    #     self.assertIn('scores', data[0])

    def test_record_emotions_post_adds_emotion_to_db(self):
        """Test that post method adds new emotion to the db."""
        from emotion_emotions.views import RecordEmotions
        num = len(Emotion.objects.all())
        request = self.request.post('', data={'image': 'data:base64,FAKE'})
        request.user = self.dan
        view = RecordEmotions(request=request)
        view.post(request)
        new_num = len(Emotion.objects.all())
        self.assertEqual(num + 1, new_num)

    def test_record_emotions_post_invalid_data_image_returns_bad_request(self):
        """Test that passing bad data into the post method returns bad request response."""
        from emotion_emotions.views import RecordEmotions
        request = self.request.post('', data={'image': 'FAKE'})
        request.user = self.dan
        view = RecordEmotions(request=request)
        response = view.post(request)
        self.assertEqual(response.content, b'Invalid data.')

    def test_record_emotions_post_invalid_data_keys_returns_bad_request(self):
        """Test that passing bad data into the post method returns bad request response."""
        from emotion_emotions.views import RecordEmotions
        request = self.request.post('', data={'face': 'data:base64,FAKE'})
        request.user = self.dan
        view = RecordEmotions(request=request)
        response = view.post(request)
        self.assertEqual(response.content, b'Invalid data.')

    def test_record_emotions_post_bad_image_to_api_returns_bad_request(self):
        """Test that passing bad image into the post method returns bad request response."""
        from emotion_emotions.views import RecordEmotions
        request = self.request.post('', data={'image': 'data:base64,FAKE'})
        request.user = self.dan
        with patch.object(RecordEmotions, 'get_emotion_data',
                          return_value={'error': {'message': 'Bad API Call'}}):
            view = RecordEmotions(request=request)
            response = view.post(request)
        self.assertEqual(response.content, b'Bad API Call')

    def test_record_emotions_route_get_has_302_not_logged_in(self):
        """Test that record emotions redirects when not logged in."""
        response = self.client.get(reverse_lazy('record_emotions'))
        self.assertEqual(response.status_code, 302)

    def test_record_emotions_route_get_redirects_to_login_not_logged_in(self):
        """Test that record emotions redirects when not logged in."""
        response = self.client.get(reverse_lazy('record_emotions'), follow=True)
        self.assertIn(str(reverse_lazy('login')), response.redirect_chain[0][0])

    def test_record_emotions_route_post_has_302_not_logged_in(self):
        """Test that record emotions redirects when not logged in."""
        response = self.client.post(reverse_lazy('record_emotions'))
        self.assertEqual(response.status_code, 302)

    def test_record_emotions_route_post_redirects_to_login_not_logged_in(self):
        """Test that record emotions redirects when not logged in."""
        response = self.client.post(reverse_lazy('record_emotions'), follow=True)
        self.assertIn(str(reverse_lazy('login')), response.redirect_chain[0][0])

    def test_record_emotions_route_get_has_200_logged_in(self):
        """Test that record emotions works when logged in."""
        self.client.login(username='dan', password='password')
        response = self.client.get(reverse_lazy('record_emotions'))
        self.assertEqual(response.status_code, 200)

    def test_emotion_analysis_route_get_has_302_not_logged_in(self):
        """Test that emotion_analysis redirects when not logged in."""
        response = self.client.get(reverse_lazy('emotion_analysis'))
        self.assertEqual(response.status_code, 302)

    def test_emotion_analysis_route_get_redirects_to_login_not_logged_in(self):
        """Test that emotion_analysis redirects when not logged in."""
        response = self.client.get(reverse_lazy('emotion_analysis'), follow=True)
        self.assertIn(str(reverse_lazy('login')), response.redirect_chain[0][0])

    def test_emotion_analysis_route_get_has_200_logged_in(self):
        """Test that emotion analysis works when logged in."""
        self.client.login(username='dan', password='password')
        response = self.client.get(reverse_lazy('emotion_analysis'))
        self.assertEqual(response.status_code, 200)

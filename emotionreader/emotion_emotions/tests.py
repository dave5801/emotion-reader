"""Test emotion app."""
from django.test import TestCase
from django.contrib.auth.models import User
from emotion_emotions.models import Emotion
import factory

import http.client, urllib.request, urllib.parse, urllib.error, base64, sys
import simplejson as json
import os
from emotion_emotions.models import Emotion


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for fake User."""

    class Meta:
        """Meta."""

        model = User

    username = factory.Sequence(lambda n:
                                '{}{}'.format(factory.Faker('first_name'), n))
    email = factory.Faker('email')


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

    # def test_emotion_route(self):
    #     """Test the emotion route."""
        

    def test_emotion_is_created_and_attached_to_user(self):
        """Test that an emotion is created and attached to a user."""
        one_user = User.objects.last()

        emotion = Emotion(user=one_user)
        emotion.anger = .1
        emotion.contempt = .2
        emotion.disgust = .3
        emotion.fear = .4
        emotion.happiness = .5
        emotion.neutral = .6
        emotion.sadness = .7
        emotion.surprise = .8
        emotion.save()

        self.assertEqual(one_user.emotion.first().anger, .1)

    # Do not want to ping API every test

    # def test_emotion_api_recieves_data_and_puts_into_database(self):
    #     """Test that the emotion api recieves data an puts it in database."""
    #     one_user = User.objects.last()

    #     headers = {
    #         'Content-Type': 'application/json',
    #         'Ocp-Apim-Subscription-Key': os.environ.get('EMOTION_API_KEY', '')
    #     }

    #     params = urllib.parse.urlencode({
    #     })

    #     body = "{ 'url': 'https://scontent-sea1-1.xx.fbcdn.net/v/t1.0-9/16998192_10211730567116496_9207760856371247359_n.jpg?oh=6e0934fb6c28dc40bdaaa52e98cef0c5&oe=5ABDE089' }"

    #     try:
    #         conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
    #         conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body, headers)
    #         response = conn.getresponse()
    #         data = response.read()

    #         parsed = json.loads(data)

    #         emotion = Emotion(user=one_user)
    #         emotion.anger = parsed[0]['scores']['anger']
    #         emotion.contempt = parsed[0]['scores']['contempt']
    #         emotion.disgust = parsed[0]['scores']['disgust']
    #         emotion.fear = parsed[0]['scores']['fear']
    #         emotion.happiness = parsed[0]['scores']['happiness']
    #         emotion.neutral = parsed[0]['scores']['neutral']
    #         emotion.sadness = parsed[0]['scores']['sadness']
    #         emotion.surprise = parsed[0]['scores']['surprise']
    #         emotion.save()

    #         conn.close()
    #     except Exception as e:
    #         print(e.args)

    #     self.assertEqual(one_user.emotion.last().anger, 1.73134707e-09)


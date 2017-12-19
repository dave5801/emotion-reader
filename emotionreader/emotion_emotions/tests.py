"""Test emotion app."""
from django.test import TestCase
from django.contrib.auth.models import User
from emotion_emotions.models import Emotion
import factory


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

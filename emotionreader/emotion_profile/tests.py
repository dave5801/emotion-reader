from django.test import TestCase
from emotion_profile.models import User, EmotionProfile
from django.core.urlresolvers import reverse_lazy

import factory


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for fake User."""

    class Meta:
        """Meta."""

        model = User

    username = factory.Sequence(lambda n:
                                '{}{}'.format(factory.Faker('first_name'), n))
    email = factory.Faker('email')


class ProfileTests(TestCase):
    """Tests for the emotion_profile module."""

    @classmethod
    def setUpClass(cls):
        """Add one minimal user to the database."""
        super(ProfileTests, cls).setUpClass()
        user = UserFactory(username='dan', email='dan@dan.net')
        user.set_password('password')
        user.first_name = 'Dan'
        user.last_name = 'Theman'
        user.save()
        cls.dan = user

    def test_profile_route_has_302_response(self):
        """Test that profile route has a 302 response code when not logged in."""
        response = self.client.get(reverse_lazy('profile'))
        self.assertEqual(response.status_code, 302)

    def test_profile_to_string_is_correct(self):
        """Test that the __str__ method returns the profile username."""
        one_profile = EmotionProfile.objects.get(user__username='dan')
        self.assertEqual(str(one_profile), 'dan')

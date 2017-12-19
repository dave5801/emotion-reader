from django.test import TestCase
from emotion_profile.models import User
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
    """Tests for the imager_profile module."""

    def test_home_route_has_200_response(self):
        """Test that home route has a 200 response code."""
        response = self.client.get(reverse_lazy('profile'))
        self.assertEqual(response.status_code, 200)

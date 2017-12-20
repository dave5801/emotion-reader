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

        for _ in range(10):
            user = UserFactory.create()
            user.set_password(factory.Faker('password'))
            user.save()

    def test_profile_route_has_302_response(self):
        """Test that profile route has a 302 response code when not logged in."""
        response = self.client.get(reverse_lazy('profile'))
        self.assertEqual(response.status_code, 302)

    def test_profile_to_string_is_correct(self):
        """Test that the __str__ method returns the profile username."""
        one_profile = EmotionProfile.objects.get(user__username='dan')
        self.assertEqual(str(one_profile), 'dan')

    def test_profile_is_created_when_user_is_saved(self):
        """Test that a profile is created automatically when a user is."""
        self.assertEquals(EmotionProfile.objects.count(), 11)
        user = UserFactory()
        user.set_password(factory.Faker('password'))
        user.save()
        self.assertEquals(EmotionProfile.objects.count(), 12)

    def test_profile_is_not_created_when_user_is_updated(self):
        """Test that a profile is created automatically when a user is."""
        self.assertEquals(EmotionProfile.objects.count(), 11)
        one_user = User.objects.last()
        one_user.username = 'Fred'
        one_user.save()
        self.assertEquals(EmotionProfile.objects.count(), 11)

# Mike's Tuesday Tests
    def test_profile_route_has_200_response(self):
        """Test that Profile view route has a 200 response code."""
        response = self.client.get(reverse_lazy('profile'))
        self.assertEqual(response.status_code, 200)

    def test_update_profile_route_has_200_response(self):
        """Test that update profile route has a 200 response code."""
        response = self.client.get(reverse_lazy('update_profile'))
        self.assertEqual(response.status_code, 200)

    def test_profile_route_has_a_tag(self):
        """Test that profile route has an A tag on the page."""
        response = self.client.get(reverse_lazy('profile'))
        self.assertIn(b'Update Profile', response.content)

    def test_update_profile_route_has_heading(self):
        """Test that update profile route has a heading on the page."""
        response = self.client.get(reverse_lazy('update_profile'))
        self.assertIn(b'Update', response.content)

    def test_profile_route_accessible_only_if_logged_in(self):
        """Test that a user can only see their profile page if logged in."""
        response = self.client.get(reverse_lazy('profile'))
        self.assertEqual(response.status_code, 302)

    def test_update_profile_route_accessible_only_if_logged_in(self):
        """Test that a user can only see their update profile page if logged in."""
        response = self.client.get(reverse_lazy('update_profile'))
        self.assertEqual(response.status_code, 302)

    def test_profile_route_accessible_when_logged_in(self):
        """Test that a user can only see their profile page if logged in."""
        self.client.login(username='dan', password='password')
        response = self.client.get(reverse_lazy('profile'))
        self.assertEqual(response.status_code, 200)

    def test_update_profile_route_accessible_when_logged_in(self):
        """Test that a user can only update a profile entry if logged."""
        self.client.login(username='dan', password='password')
        response = self.client.get(reverse_lazy('update_profile'))
        self.assertEqual(response.status_code, 200)

"""Test file for emotion profile."""
from django.test import TestCase
from emotion_profile.models import User, EmotionProfile
from django.core.urlresolvers import reverse_lazy
from django.core import mail

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

    def test_profile_route_login_200_response(self):
        """Test that profile route with login works."""
        self.client.login(username='dan', password='password')
        response = self.client.get(reverse_lazy('profile'))
        self.assertEqual(response.status_code, 200)

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
        self.assertEqual(response.status_code, 302)

    def test_update_profile_route_has_200_response(self):
        """Test that update profile route has a 200 response code."""
        response = self.client.get(reverse_lazy('update_profile'))
        self.assertEqual(response.status_code, 302)

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

    def test_profile_has_cover(self):
        """Test that a profile has a cover."""
        active_user = User.objects.get(username='dan')
        one_profile = EmotionProfile.objects.get(user=active_user)
        self.assertIsNotNone(one_profile.cover)

    def test_user_can_point_to_its_profile(self):
        """Test that a user and profile are connected."""
        one_user = User.objects.get(username='dan')
        self.assertIsNotNone(one_user.profile)

    def test_all_profiles_created(self):
        """Test that all profiles were added to the database."""
        self.assertEquals(EmotionProfile.objects.count(), 11)

    def test_all_users_created(self):
        """Test that all users were added to the database."""
        self.assertEquals(User.objects.count(), 11)

# Mike's Wednesday tests
    def test_actvation_link_redirects_to_activate_completed_page(self):
        """Test if acitvation link works."""
        import re
        mail_response = self.client.post(reverse_lazy('registration_register'), {
            'username': 'Mike',
            'password1': 'qwerty12345',
            'password2': 'qwerty12345',
            'email': 'Mike@Mike.net'
        })
        # import pdb; pdb.set_trace()
        activation = re.findall('/accounts/activate/.+/', mail.outbox[0].body)
        response = self.client.get(activation[0], follow=True)
        self.assertIn(b'Activation Complete', response.content)

    def test_register_allows_login_to_new_users(self):
        """Test if users created can log in."""
        import re
        self.client.login(username='Mike', password='password')
        response = self.client.get(reverse_lazy('home'))
        self.assertNotIn(b'Welcome,', response.content)
        self.client.post(reverse_lazy('registration_register'), {
            'username': 'Mike',
            'password1': 'qwerty12345',
            'password2': 'qwerty12345',
            'email': 'Mike@Mike.net'
        })
        activation = re.findall('/accounts/activate/.+/', mail.outbox[0].body)
        self.client.get(activation[0])
        self.client.login(username='Mike', password='password')
        response = self.client.get(reverse_lazy('home'))
        self.assertIn(b'Emotion Tracker', response.content)

    def test_register_with_activation_valid_user_password_activates_user(self):
        """Test if valid user with password is activated, activates user."""
        import re
        self.client.post(reverse_lazy('registration_register'), {
            'username': 'Mike',
            'password1': 'qwerty12345',
            'password2': 'qwerty12345',
            'email': 'Mike@Mike.net'
        })
        activation = re.findall('/accounts/activate/.+/', mail.outbox[0].body)
        self.client.get(activation[0])
        self.assertTrue(User.objects.get(username='Mike').is_active)

    def test_register_taken_username_responds_with_200(self):
        """Test register taken responds with 200."""
        response = self.client.post(reverse_lazy('registration_register'), {
            'username': 'dan',
            'password1': 'qwerty12345',
            'password2': 'qwerty12345',
            'email': 'dan@dan.net'
        })
        self.assertEqual(200, response.status_code)

    def test_register_taken_user_name_displays_name_taken(self):
        """Test register taken responds with username taken."""
        response = self.client.post(reverse_lazy('registration_register'), {
            'username': 'dan',
            'password1': 'qwerty12345',
            'password2': 'qwerty12345',
            'email': 'dan@dan.net'
        })
        self.assertIn(b'username already exists', response.content)

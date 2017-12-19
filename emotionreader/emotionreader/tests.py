"""Tests."""
from django.test import TestCase
from django.core.urlresolvers import reverse_lazy
from emotion_profile.tests import UserFactory


class MainRoutingTests(TestCase):
    """Tests for the routes in imagersite."""

    def setUp(self):
        """Set up a user for testing login.."""
        user = UserFactory(username='bob', email='bob@bob.net')
        user.set_password('password')
        user.save()

    def test_home_route_has_200_response(self):
        """Test that home route has a 200 response code."""
        response = self.client.get(reverse_lazy('home'))
        self.assertEqual(response.status_code, 200)

    def test_login_get_has_200_response(self):
        """Test that login get route has a 200 response code."""
        response = self.client.get(reverse_lazy('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_get_login_form(self):
        """Test that login get route has a login form."""
        response = self.client.get(reverse_lazy('login'))
        self.assertIn(b'<h1>Login</h1>', response.content)

    def test_login_post_invalid_user_has_200_response(self):
        """Test that login with invalid username has a 200 response code."""
        response = self.client.post(reverse_lazy('login'), {
            'username': 'fred',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 200)

    def test_login_post_invalid_user_displays_invalid_login(self):
        """Test that login with invalid username displays to bad login."""
        response = self.client.post(reverse_lazy('login'), {
            'username': 'fred',
            'password': 'password'
        })
        self.assertIn(b'Please enter a correct username', response.content)

    def test_login_post_invalid_password_has_200_response(self):
        """Test that login with invalid username has a 200 response code."""
        response = self.client.post(reverse_lazy('login'), {
            'username': 'bob',
            'password': 'passwordssss'
        })
        self.assertEqual(response.status_code, 200)

    def test_login_post_invalid_password_displays_invalid_login(self):
        """Test that login with invalid username displays to bad login."""
        response = self.client.post(reverse_lazy('login'), {
            'username': 'bob',
            'password': 'passwordssss'
        })
        self.assertIn(b'Please enter a correct username', response.content)

    def test_login_post_valid_login_has_302_response(self):
        """Test that login with valid login has a 302 response code."""
        response = self.client.post(reverse_lazy('login'), {
            'username': 'bob',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 302)

    def test_login_post_validates_users(self):
        """Test that login validates users."""
        response = self.client.get(reverse_lazy('home'))
        self.assertNotIn(b'bob </a>', response.content)
        self.client.post(reverse_lazy('login'), {
            'username': 'bob',
            'password': 'password'
        })
        response = self.client.get(reverse_lazy('home'))
        self.assertIn(b'bob </a>', response.content)

    def test_login_post_valid_login_redirects_to_profile_page(self):
        """Test that login with valid login redirects to home page."""
        response = self.client.post(reverse_lazy('login'), {
            'username': 'bob',
            'password': 'password'
        }, follow=True)
        self.assertEqual(response.redirect_chain[0][0], reverse_lazy('profile'))

    def test_logout_get_has_302_response(self):
        """Test that logout get route has a 302 response code."""
        response = self.client.get(reverse_lazy('logout'))
        self.assertEqual(response.status_code, 302)

    def test_logout_get_has_redirects_home(self):
        """Test that logout get route has logged-out title."""
        response = self.client.get(reverse_lazy('logout'), follow=True)
        self.assertEqual(response.redirect_chain[0][0], reverse_lazy('home'))

    def test_logout_from_login_user_will_logsout_user(self):
        """Test that logout will redirects to logout page."""
        self.client.login(username='bob', password='password')
        response = self.client.get(reverse_lazy('home'))
        self.assertIn(b'bob </a>', response.content)
        self.client.get(reverse_lazy('logout'))
        response = self.client.get(reverse_lazy('home'))
        self.assertNotIn(b'bob </a>', response.content)

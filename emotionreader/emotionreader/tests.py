"""Tests."""
from django.test import TestCase
from django.core.urlresolvers import reverse_lazy


class MainRoutingTests(TestCase):
    """Tests for the routes in imagersite."""

    def test_home_route_has_200_response(self):
        """Test that home route has a 200 response code."""
        response = self.client.get(reverse_lazy('home'))
        self.assertEqual(response.status_code, 200)

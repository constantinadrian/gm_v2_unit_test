from django.test import TestCase
from django.urls import reverse, resolve

from home.views import index


class TestHomeUrls(TestCase):
    """
    Test for home urls
    """

    def test_home_url(self):
        """
        Test for home url
        """
        url = reverse('home')
        self.assertEqual(resolve(url).func, index)

from django.test import TestCase
from django.urls import reverse, resolve

from profiles.views import profile, order_history


class TestProfilesUrls(TestCase):
    """
    Test for Urls for profiles app
    """

    def test_profile_url(self):
        """
        Test profile url
        """
        url = reverse('profile')
        self.assertEqual(resolve(url).func, profile)

    def test_order_history_url(self):
        """
        Test order history url
        """
        url = reverse(
            'order_history',
            kwargs={'order_number': 'SAD657ASDA723762133SA'}
        )
        self.assertEqual(resolve(url).func, order_history)

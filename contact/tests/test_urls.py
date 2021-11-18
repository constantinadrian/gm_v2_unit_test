from django.test import TestCase
from django.urls import reverse, resolve

from contact.views import contact


class TestContactUrls(TestCase):
    """
    Test Urls for contact app
    """

    def test_contact_url(self):
        """
        Test contact url
        """
        url = reverse('contact')
        self.assertEqual(resolve(url).func, contact)

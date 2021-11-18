from django.test import TestCase
from django.urls import reverse, resolve

from newsletter.views import newsletter_signup


class TestNewsLetterSignUpUrls(TestCase):
    """
    Test Urls for Newsletter app
    """

    def test_newsletter_signup_url(self):
        """
        Test newsletter signup url
        """
        url = reverse('newsletter_signup')
        self.assertEqual(resolve(url).func, newsletter_signup)

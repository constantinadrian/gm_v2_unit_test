from django.test import TestCase

from newsletter.models import Newsletter


class TestNewsletterModels(TestCase):
    """
    Test for Newsletter models
    """

    def setUp(self):
        self.email = 'test.test@example.com'

    def test_newsletter_model(self):
        """
        Test for Newsletter model str
        """
        newsletter = Newsletter.objects.create(email=self.email)
        self.assertEqual(str(newsletter), newsletter.email)

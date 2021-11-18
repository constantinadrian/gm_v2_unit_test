from django.test import TestCase

from newsletter.forms import NewsletterForm


class TestNewsletterForms(TestCase):
    """
    Test for Newsletter forms
    """

    def setUp(self):
        self.email = 'test.test@example.com'

    def test_newsletter_form_with_invalid_data(self):
        """
        Test newsletter form with invalid data
        """
        form = NewsletterForm({
            "email": ""
        })

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors.keys())
        self.assertEqual(form.errors["email"][0], "This field is required.")

    def test_newsletter_form_with_valid_data(self):
        """
        Test newsletter form with valid data
        """
        form = NewsletterForm({
            "email": self.email
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.clean_email(), self.email)
